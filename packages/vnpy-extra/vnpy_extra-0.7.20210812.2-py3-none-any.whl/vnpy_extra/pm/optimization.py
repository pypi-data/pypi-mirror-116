"""
@author  : MG
@Time    : 2021/7/21 15:06
@File    : optimization.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
from collections import defaultdict
from enum import Enum
from typing import List, Set, Dict, Optional

import cvxpy
import pandas as pd
from ibats_utils.transfer import str_2_date
from pypfopt import EfficientFrontier, risk_models, expected_returns, DiscreteAllocation

from vnpy_extra.backtest import InstrumentClassificationEnum
from vnpy_extra.db.export_strategy_setting import generate_strategy_setting_file
from vnpy_extra.db.orm import SymbolsInfo, AccountStrategyMapping, StrategyBacktestStats, set_account
from vnpy_extra.pm.plot import plot_with_weights
from vnpy_extra.utils.symbol import get_vt_symbol_multiplier, get_instrument_type


class PortfolioOptimizeGoalEnum(Enum):
    max_sharpe = 'max_sharpe'
    min_volatility = 'min_volatility'
    max_quadratic_utility = 'max_quadratic_utility'
    equal_mdd = 'equal_mdd'


class PortfolioOptimization:

    def __init__(self, stats_list: List[StrategyBacktestStats], goal: Optional[PortfolioOptimizeGoalEnum] = None,
                 **kwargs):
        self.key_stats_dic: Dict[str, StrategyBacktestStats] = {_.get_stats_key_str(): _ for _ in stats_list}
        # 目前仅考虑 CTA 的情况
        self.key_vt_symbol_dic: Dict[str, str] = {
            key: _.symbols_info.symbols for key, _ in self.key_stats_dic.items()}
        self.key_multiplier_dic = {
            key: get_vt_symbol_multiplier(_.symbols_info.symbols) for key, _ in self.key_stats_dic.items()}
        self.key_balance_df_dic: Dict[str, pd.DataFrame] = {
            key: _.get_balance_df() for key, _ in self.key_stats_dic.items()}
        date_range_df = pd.DataFrame({
            key: [df.index.min(), df.index.max(), df.index.max() - df.index.min()]
            for key, df in self.key_balance_df_dic.items() if df is not None}, index=['start', 'end', 'range']).T
        min_range_s = date_range_df.iloc[date_range_df['range'].argmin(), :]
        self.profit_df = pd.DataFrame({
            key: df['profit']
            for key, df in self.key_balance_df_dic.items() if df is not None}).dropna()
        self.ef = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"最短周期策略为："
                         f"{min_range_s.name}[{min_range_s['range']}] {min_range_s['start']} - {min_range_s['end']}")
        self.goal = goal
        self.key_weight_dic: Optional[Dict] = None
        self._kwargs = kwargs
        self.group_weight_dic: Optional[Dict[InstrumentClassificationEnum, float]] = None
        self.auto_merge_into_other_group_if_lower_than = 1
        self.max_vt_symbol_weight = None
        self.start_date = None

    def set_goal(self, goal, fit_by_group: Optional[Dict[InstrumentClassificationEnum, float]] = None,
                 max_vt_symbol_weight=None, start_date=None, **kwargs):
        self.goal = goal
        self.group_weight_dic: Optional[Dict[InstrumentClassificationEnum, float]] = fit_by_group
        self.max_vt_symbol_weight = max_vt_symbol_weight
        self.start_date = start_date
        self._kwargs.update(kwargs)

    def fit(self):
        if self.group_weight_dic:
            # 分组计算权重
            group_keys_dic = {}
            group_merged_key_set = {}
            min_group = None
            for group, weight in list(self.group_weight_dic.items()):
                key_set = set([
                    key for key, vt_symbol in self.key_vt_symbol_dic.items()
                    if key in self.key_balance_df_dic and get_instrument_type(vt_symbol).upper() in group.value])
                key_count = len(key_set)
                if key_count == 0:
                    self.group_weight_dic.pop(group)
                    self.logger.warning(f"{group.name} has {key_count} key. ignored.")
                    continue
                elif key_count == 1 and self.auto_merge_into_other_group_if_lower_than <= 0:
                    raise ValueError(f"{group.name} has only on key '{key_set.pop()}'")
                elif key_count <= self.auto_merge_into_other_group_if_lower_than:
                    self.logger.warning(f"{group.name} has {key_count} keys too small to be optimized.")
                    group_merged_key_set[group] = (key_set, weight)
                else:
                    group_keys_dic[group] = key_set
                    if not min_group or len(group_keys_dic[min_group]) > key_count:
                        min_group = group

            if len(group_merged_key_set) > 0:
                # 数量过少的 key 集中到一起合并到此前最少的分组里面
                for group, (key_set, weight) in group_merged_key_set.items():
                    self.logger.warning(
                        f"{len(group_merged_key_set)} keys merge {group} -> {min_group.name}: {key_set}")
                    self.group_weight_dic[min_group] += weight
                    group_keys_dic[min_group].update(key_set)

            tot_weight = sum(self.group_weight_dic.values())
            self.group_weight_dic = {group: weight / tot_weight for group, weight in self.group_weight_dic.items()}
            msg = "\n".join(
                [f"{group.name:50s} {weight * 100:.2f}%" for group, weight in self.group_weight_dic.items()])
            self.logger.info(f"各分组权重如下：\n{msg}")
        else:
            # 不分组计算权重
            group_keys_dic = {'all': self.key_balance_df_dic.keys()}

        # 分组进行目标优化
        key_weight_dic = {}
        for group, key_set in group_keys_dic.items():
            # 更新 key_weight_dic 记录
            self._fit_by_group_keys(key_weight_dic, group, key_set)

        _sum = sum(key_weight_dic.values())
        keys = list(key_weight_dic.keys())
        keys.sort()
        self.key_weight_dic = _key_weight_dic = {key: key_weight_dic[key] / _sum for key in keys}
        if self.max_vt_symbol_weight:
            # -------------------- max_vt_symbol_weight 调整开始 ----------------------------
            # 记录因仓位限制而调整后，剩余的key以及仓位比例
            rest_key_set = set(_key_weight_dic.keys())
            rest_weight = 1
            # 按 instrument_type 分组
            vt_symbol_weight_pairs_dic = defaultdict(list)
            for key, weight in _key_weight_dic.items():
                vt_symbol_weight_pairs_dic[self.key_vt_symbol_dic[key]].append(
                    (key, weight))

            # 分组计算是否需要调整
            vt_symbol_weight_dic = {}
            for vt_symbol, key_weight_pairs in vt_symbol_weight_pairs_dic.items():
                tot_weight = sum([_[1] for _ in key_weight_pairs])
                if tot_weight > self.max_vt_symbol_weight:
                    scaling_down_rate = self.max_vt_symbol_weight / tot_weight
                    for key, weight in key_weight_pairs:
                        _key_weight_dic[key] = weight * scaling_down_rate
                        rest_key_set.remove(key)

                    keys_str = '\n'.join([f"{key:130s} {weight * 100:.2f}% -> {_key_weight_dic[key] * 100:.2f}"
                                          for key, weight in key_weight_pairs])
                    self.logger.warning(
                        f"{vt_symbol} 总体比例 {tot_weight * 100:.2f}% > "
                        f"{self.max_vt_symbol_weight * 100:.2f}% 缩放比例 {scaling_down_rate:.2f}，"
                        f"受影响key包括：\n{keys_str}")
                    rest_weight -= self.max_vt_symbol_weight
                    vt_symbol_weight_dic[vt_symbol] = self.max_vt_symbol_weight
                else:
                    vt_symbol_weight_dic[vt_symbol] = tot_weight

            if rest_weight < 1:
                tot_weight = sum([weight for key, weight in self.key_weight_dic.items() if key in rest_key_set])
                change_rate = rest_weight / tot_weight
                self.logger.warning(f"调整剩余 {len(rest_key_set)} key 的权重，调整因子{change_rate:.2f}")
                # 按合约简称是否存在调整后超 max_vt_symbol_weight 的合约
                vt_symbols = list({self.key_vt_symbol_dic[key] for key in rest_key_set})
                vt_symbols.sort(key=lambda x: vt_symbol_weight_dic[x], reverse=True)
                for vt_symbol in vt_symbols:
                    vt_symbol_weight = vt_symbol_weight_dic[vt_symbol]
                    new_weight = vt_symbol_weight * change_rate
                    if new_weight > self.max_vt_symbol_weight:
                        change_rate_curr = self.max_vt_symbol_weight / vt_symbol_weight
                        tot_weight -= vt_symbol_weight
                        rest_weight -= self.max_vt_symbol_weight
                        change_rate = rest_weight / tot_weight
                        change_rate_changed = True
                    else:
                        change_rate_curr = change_rate
                        change_rate_changed = False

                    key_weight_pairs = vt_symbol_weight_pairs_dic[vt_symbol]
                    for key, weight in key_weight_pairs:
                        self.key_weight_dic[key] = weight * change_rate_curr
                        rest_key_set.remove(key)

                    if change_rate_changed:
                        self.logger.warning(
                            f"调整剩余 {len(rest_key_set)} key 的权重，"
                            f"调整因子{change_rate:.2f}，{vt_symbol} -> {self.max_vt_symbol_weight * 100:.2f}%")

            # -------------------- max_vt_symbol_weight 调整结束 ----------------------------

        self.logger.info(f"{'*' * 20} weight by key {'*' * 20}")
        for num, (key, weight) in enumerate(self.key_weight_dic.items(), start=1):
            self.logger.info(f"{num:2d}) {self.key_vt_symbol_dic[key]:11s} {key:130s} --> {weight * 100:.2f}%")

        self.logger.info(f"{'*' * 20} weight by vt_symbol {'*' * 20}")
        vt_symbol_weight_pairs_dic = defaultdict(list)
        for key, weight in self.key_weight_dic.items():
            vt_symbol_weight_pairs_dic[self.key_vt_symbol_dic[key]].append((key, weight))
        vt_symbols = list(vt_symbol_weight_pairs_dic.keys())
        vt_symbols.sort()
        for num, vt_symbol in enumerate(vt_symbols, start=1):
            key_weight_pairs = vt_symbol_weight_pairs_dic[vt_symbol]
            tot_weight = sum([_[1] for _ in key_weight_pairs])
            self.logger.info(f"{num:2d}) {vt_symbol:11s}[{len(key_weight_pairs)}] --> {tot_weight * 100:.2f}%")

    def _fit_by_group_keys(self, key_weight_dic, group, key_set: set):
        if self.goal == PortfolioOptimizeGoalEnum.equal_mdd:
            key_mdd_dic = {
                key: _.indicator_dic.get("daily_stats_dic", {}).get("max_drawdown", None)
                for key, _ in self.key_stats_dic.items()
                if (key in key_set and _.indicator_dic and
                    _.indicator_dic.get("daily_stats_dic", {}).get("max_drawdown", None) is not None)
            }
            benchmark_capital = self._kwargs.get('benchmark', 100_000)
            key_weight_dic.update({key: benchmark_capital / v * self.group_weight_dic[group]
                                   for key, v in key_mdd_dic.items()})
        else:
            balance_df = pd.DataFrame({
                key: df['balance']
                for key, df in self.key_balance_df_dic.items() if key in key_set and df is not None}).dropna()
            if self.start_date:
                balance_df = balance_df[balance_df.index >= pd.to_datetime(self.start_date)]
            count = balance_df.shape[1]
            mu = expected_returns.mean_historical_return(balance_df)
            sample_cov = risk_models.sample_cov(balance_df)
            # Optimize for maximal Sharpe ratio
            self.ef = EfficientFrontier(
                mu, sample_cov, weight_bounds=(0, 0.3) if count > 4 else (0, 1), solver=cvxpy.ECOS)
            raw_weights = getattr(self.ef, self.goal.value)()
            # self.ef.save_weights_to_file("weights.csv")  # saves to file
            # self.ef.portfolio_performance(verbose=True)  #
            _key_weight_dic = {
                key: weight * self.group_weight_dic[group]
                # for key, weight in self.ef.clean_weights().items()
                for key, weight in raw_weights.items()
            }
            key_weight_dic.update(_key_weight_dic)
            self.logger.info(f"{group.name} has {len(raw_weights)} keys")
            for num, (key, weight) in enumerate(raw_weights.items(), start=1):
                self.logger.info(f"{num:2d}) {self.key_vt_symbol_dic[key]:11s} {key:130s} --> {weight * 100:.2f}%")

    def get_weights(self) -> Dict[str, float]:
        return self.key_weight_dic

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
    capital = 3_000_000
    set_account(user_name, broker_id)
    po = PortfolioOptimization.build_by_account(user_name, broker_id)
    po.set_goal(
        PortfolioOptimizeGoalEnum.equal_mdd,
        benchmark=20_000,  # 仅 PortfolioOptimizeGoalEnum.equal_mdd 时有效
        fit_by_group={
            InstrumentClassificationEnum.AGRICULTURE: 0.2,
            InstrumentClassificationEnum.CHEMICAL: 0.3,
            InstrumentClassificationEnum.CFFEX: 0.2,
            InstrumentClassificationEnum.BLACK: 0.4,
            InstrumentClassificationEnum.PRECIOUS_NONFERROUS_METAL: 0.1,
        },
        start_date=str_2_date('2021-01-01'),
        max_vt_symbol_weight=0.2
    )
    # po.set_goal(PortfolioOptimizeGoalEnum.equal_mdd, benchmark=100_000)
    po.fit()
    # po.logger.info(pd.DataFrame([po.get_base_positions()]).T)
    plot_with_weights(
        po.key_stats_dic.values(), po.get_base_positions(capital=capital),
        capital=capital, key_vt_symbol_dic=po.key_vt_symbol_dic)
    if do_update_base_positions:
        po.update_base_positions(
            min_positions=0, stop_opening_pos_if_base_position_zero=True,
            capital=capital)
        generate_strategy_setting_file(
            list(po.key_stats_dic.values()), ignore_stop_opening_pos_stg=True)


if __name__ == "__main__":
    _test_po()
