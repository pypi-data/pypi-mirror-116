"""
@author  : MG
@Time    : 2021/7/21 15:06
@File    : optimization.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
from enum import Enum
from typing import List, Set, Dict, Optional

import cvxpy
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns, DiscreteAllocation

from vnpy_extra.db.export_strategy_setting import generate_strategy_setting_file
from vnpy_extra.db.orm import SymbolsInfo, AccountStrategyMapping, StrategyBacktestStats, set_account
from vnpy_extra.pm.plot import plot_with_weights
from vnpy_extra.utils.symbol import get_vt_symbol_multiplier


class PortfolioOptimizeGoalEnum(Enum):
    max_sharpe = 'max_sharpe'
    min_volatility = 'min_volatility'
    max_quadratic_utility = 'max_quadratic_utility'
    equal_mdd = 'equal_mdd'


class PortfolioOptimization:

    def __init__(self, stats_list: List[StrategyBacktestStats], goal: Optional[PortfolioOptimizeGoalEnum]=None, **kwargs):
        self.key_stats_dic: Dict[str, StrategyBacktestStats] = {_.get_stats_key_str(): _ for _ in stats_list}
        # 目前仅考虑 CTA 的情况
        self.key_multiplier_dic = {
            key: get_vt_symbol_multiplier(_.symbols_info.symbols)
            for key, _ in self.key_stats_dic.items()}
        self.key_balance_df_dic: Dict[str, pd.DataFrame] = {
            key: _.get_balance_df() for key, _ in self.key_stats_dic.items()}

        date_range_df = pd.DataFrame({
            key: [df.index.min(), df.index.max(), df.index.max() - df.index.min()]
            for key, df in self.key_balance_df_dic.items() if df is not None}, index=['start', 'end', 'range']).T
        min_range_s = date_range_df.iloc[date_range_df['range'].argmin(), :]
        print(f"最短周期策略为 {min_range_s.name}[{min_range_s['range']}] {min_range_s['start']} - {min_range_s['end']}")
        self.profit_df = pd.DataFrame({
            key: df['profit']
            for key, df in self.key_balance_df_dic.items() if df is not None}).dropna()
        self.ef = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.goal = goal
        self.weights_dic: Optional[Dict] = None
        self._kwargs = kwargs

    def set_goal(self, goal, **kwargs):
        self.goal = goal
        self._kwargs.update(kwargs)

    def fit(self):
        if self.goal == PortfolioOptimizeGoalEnum.equal_mdd:
            key_mdd_dic = {
                key: _.indicator_dic.get("daily_stats_dic", {}).get("max_drawdown", None)
                for key, _ in self.key_stats_dic.items()
                if _.indicator_dic and _.indicator_dic.get("daily_stats_dic", {}).get("max_drawdown", None) is not None
            }
            benchmark_capital = self._kwargs.get('benchmark', 100_000)
            weights_dic = {key: benchmark_capital / v for key, v in key_mdd_dic.items()}
            _sum = sum(weights_dic.values())
            self.weights_dic = {key: v / _sum for key, v in weights_dic.items()}
        else:
            balance_df = pd.DataFrame({
                key: df['balance']
                for key, df in self.key_balance_df_dic.items() if df is not None}).dropna()
            mu = expected_returns.mean_historical_return(balance_df)
            sample_cov = risk_models.sample_cov(balance_df)
            # Optimize for maximal Sharpe ratio
            self.ef = EfficientFrontier(mu, sample_cov, weight_bounds=(0, 0.3), solver=cvxpy.ECOS)
            raw_weights = getattr(self.ef, self.goal.value)()
            # self.ef.save_weights_to_file("weights.csv")  # saves to file
            # self.ef.portfolio_performance(verbose=True)  #
            self.weights_dic = self.ef.clean_weights()

        print('*' * 20, 'weights', '*' * 20)
        for num, (name, weight) in enumerate(self.weights_dic.items(), start=1):
            print(f"{num:2d}) {name} --> {weight * 100:.1f}%")

    def get_weights(self) -> Dict[str, float]:
        return self.weights_dic

    def get_latest_price(self) -> Dict[str, float]:
        symbols: Set[str] = {_.symbols_info.symbols.split('.')[0] for _ in self.key_stats_dic.values()}
        symbol_price_dic = SymbolsInfo.get_symbol_latest_price_dic(symbols)
        return symbol_price_dic

    def get_base_positions(self, capital=1_000_000) -> Dict[str, int]:
        symbol_price_dic = self.get_latest_price()
        # 该价格为×乘数后的价格
        weights_dic = self.get_weights()
        price_s = pd.Series({
            k: symbol_price_dic[
                   stats.symbols_info.symbols.split('.')[0].upper()
               ] * get_vt_symbol_multiplier(stats.symbols_info.symbols)
            for k, stats in self.key_stats_dic.items() if k in weights_dic})
        da = DiscreteAllocation(weights_dic, price_s, capital)
        key_base_positions_dic, leftover = da.lp_portfolio()
        print('*' * 20, 'base_positions', capital, '*' * 20)
        for num, (key, base_positions) in enumerate(key_base_positions_dic.items(), start=1):
            print(f"{num:2d}) {key} --> {base_positions}")
        return key_base_positions_dic

    def plot_fitted(self, *, legend=False):

        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 24))
        axes = axes.flatten()
        self.profit_df[[
            k for k, v in self.get_weights().items() if v > 0.0001
        ]].plot(grid=True, ax=axes[0])
        result = pd.DataFrame([self.profit_df[k] * v for k, v in self.get_weights().items()]).sum(axis=0)
        result.plot(grid=True, ax=axes[1])
        plt.show()

    def update_base_positions(self, *, capital=1_000_000, min_positions=0,
                              stop_opening_pos_if_base_position_zero=False):
        from vnpy_extra.db.orm import database
        with database.atomic():
            key_base_positions_dic = self.get_base_positions(capital=capital)
            for key, stats in self.key_stats_dic.items():
                base_positions = key_base_positions_dic.get(key, min_positions)
                stats.set_base_position(
                    base_positions, stop_opening_pos_if_base_position_zero=stop_opening_pos_if_base_position_zero)

    @staticmethod
    def build_by_account(user_name, broker_id):
        stats_list = AccountStrategyMapping.get_stats_by_account(
            user_name, broker_id)
        return PortfolioOptimization(stats_list)


def _test_po():
    do_update_base_positions = False
    user_name, broker_id = "11859087", "95533"
    capital = 2_000_000
    set_account(user_name, broker_id)
    po = PortfolioOptimization.build_by_account(user_name, broker_id)
    # po.set_goal(PortfolioOptimizeGoalEnum.min_volatility)
    po.set_goal(PortfolioOptimizeGoalEnum.equal_mdd, benchmark=100_000)
    po.fit()
    # po.logger.info(pd.DataFrame([po.get_base_positions()]).T)
    plot_with_weights(po.key_stats_dic.values(), po.get_base_positions(capital=capital))
    if do_update_base_positions:
        po.update_base_positions(
            min_positions=0, stop_opening_pos_if_base_position_zero=True,
            capital=capital)
        generate_strategy_setting_file(
            list(po.key_stats_dic.values()), ignore_stop_opening_pos_stg=True)


if __name__ == "__main__":
    _test_po()
