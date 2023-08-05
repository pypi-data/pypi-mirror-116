#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/8/2 8:52
@File    : plot.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from typing import Dict, Callable

import matplotlib.pyplot as plt
import pandas as pd

from vnpy_extra.constants import BASE_POSITION, STOP_OPENING_POS_PARAM
from vnpy_extra.db.orm import StrategyBacktestStats, set_account, AccountStrategyMapping


def get_strategy_settings_by_account(stats: StrategyBacktestStats):
    return getattr(stats, 'strategy_settings_of_account', stats.strategy_settings)


def get_strategy_settings_by_default(stats: StrategyBacktestStats):
    return stats.strategy_settings


def plot_with_weights(stats_list, weight_dic: dict):
    key_stats_dic: Dict[str, StrategyBacktestStats] = {_.get_stats_key_str(): _ for _ in stats_list}
    key_df_dic = {
        key: stats.get_balance_df()
        for key, stats in key_stats_dic.items()}
    # profit_df = pd.DataFrame({key: df['profit'] for key, df in key_df_dic.items() if df is not None}).dropna()
    balance_df = pd.DataFrame({key: df['balance'] for key, df in key_df_dic.items() if df is not None}).dropna()
    rr_df = balance_df/balance_df.iloc[0,:]
    # for key, stats in key_stats_dic.items():
    #     if STOP_OPENING_POS_PARAM not in get_strategy_settings(stats):
    #         print(key, get_strategy_settings(stats))

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 24))
    axes = axes.flatten()
    rr_sub_df = rr_df[[
        key for key, weight in weight_dic.items()
        if weight > 0.0001
    ]]
    rr_sub_df.plot(grid=True, ax=axes[0])
    result = pd.DataFrame([
        rr_sub_df[key] * weight
        for key, weight in weight_dic.items()
    ]).sum(axis=0)
    (result/result.iloc[0]).plot(grid=True, ax=axes[1])
    plt.show()


def plot_with_base_position(
        stats_list,
        get_strategy_settings_func: Callable[[StrategyBacktestStats], dict] = get_strategy_settings_by_default):
    """根据权重合并 profit plot 出合并后的 profit 曲线"""

    base_position_dic = {
        _.get_stats_key_str(): get_strategy_settings_func(_).get(BASE_POSITION, 1)
        for _ in stats_list if not get_strategy_settings_func(_).get(STOP_OPENING_POS_PARAM, 0)}
    plot_with_weights(stats_list=stats_list, weight_dic=base_position_dic)


def _test_plot_with_weights():
    user_name, broker_id = "11859087", "95533"
    set_account(user_name, broker_id)
    stats_list = AccountStrategyMapping.get_stats_by_account(
        user_name, broker_id)
    plot_with_base_position(stats_list, get_strategy_settings_func=get_strategy_settings_by_account)


if __name__ == "__main__":
    _test_plot_with_weights()
