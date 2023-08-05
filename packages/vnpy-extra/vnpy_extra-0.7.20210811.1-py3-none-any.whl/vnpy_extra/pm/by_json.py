#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/8/10 11:17
@File    : by_json.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import json

from vnpy_extra.db.orm import StrategyBacktestStats, SymbolsInfo, set_account, StrategyBacktestStatusEnum, \
    AccountStrategyMapping
from vnpy_extra.pm.plot import plot_with_base_position
from vnpy_extra.utils.symbol import get_main_contract


def get_id_name_symbol(name: str):
    """通过name拆分冲 id_name, symbol（仅支持合约）"""
    # 以下方法存在较严重偏差，容易与参数发生混淆
    # idx = 0
    # for _ in name.split('_')[::-1]:
    #     if PATTERN_INSTRUMENT_TYPE_RESTRICT.match(_):
    #         idx += len(_) + 1
    #     else:
    #         break
    #
    # if idx == 0:
    #     raise ValueError(f"{name}不是有效的名称")
    # id_name, symbol = name[:-idx], name[-idx + 1:]
    idx = name[::-1].find('_')
    id_name, symbol = name[:-idx - 1], name[-idx:]
    return id_name, symbol


def get_merged_profit_by_json(json_file_path: str, encoding='utf-8'):
    """根据json文件中的策略名称，找到对应策略曲线拟合出合并后的收益率曲线"""
    with open(json_file_path, encoding=encoding) as f:
        name_setting_dic = json.load(f)

    stats_list = []
    for name, setting_dic in name_setting_dic.items():
        id_name, symbol_str = get_id_name_symbol(name)
        si_obj = SymbolsInfo.get_by_symbol_str(symbol_str)
        stats_list.append(StrategyBacktestStats.get_by_id_name_and_symbol_info(id_name, si_obj))

    plot_with_base_position(stats_list=stats_list)


def _run_get_merged_profit_by_json():
    json_file_path = r"F:\downloads\马过转换主力合约后的setting.json"
    get_merged_profit_by_json(json_file_path)


def add_stg_2_account_by_json(user_name: str, broker_id: str, json_file_path: str, encoding='utf-8'):
    set_account(user_name, broker_id)
    with open(json_file_path, encoding=encoding) as f:
        name_setting_dic = json.load(f)
    stg_short_num_dic = {}
    for name, setting_dic in name_setting_dic.items():
        id_name, symbol_str = get_id_name_symbol(name)
        vt_symbol = setting_dic.get('vt_symbol', None)
        if not vt_symbol:
            vt_symbol = setting_dic.get('vt_symbols', None)
        if not vt_symbol:
            raise ValueError("setting_dic 缺少 vt_symbol/vt_symbols 字段")

        si_obj: SymbolsInfo = SymbolsInfo.get_instance(vt_symbol)
        main_vt_symbol = get_main_contract(si_obj.symbols)
        si_main_obj = SymbolsInfo.get_instance(main_vt_symbol)
        stats_main: StrategyBacktestStats = StrategyBacktestStats.get_by_id_name_and_symbol_info(id_name, si_main_obj)
        stats_main.update_backtest_status(
            StrategyBacktestStatusEnum.QuasiOnline,
            remark_4_log=si_main_obj.symbols,
            stg_short_num_dic=stg_short_num_dic,
        )
        AccountStrategyMapping.add_2_account(
            stg_info_id=stats_main.stg_info_id,
            symbols_info_id=si_obj.id,
            id_name=stats_main.id_name,
            short_name=name,
            shown_name=name,
            strategy_settings={k: v for k, v in setting_dic['setting'].items() if k not in ('class_name',)},
        )


def _run_add_stg_2_account():
    user_name, broker_id = "0", "0"
    json_file_path = r"F:\downloads\cta_strategy_setting.json"
    add_stg_2_account_by_json(user_name, broker_id, json_file_path)


if __name__ == "__main__":
    _run_get_merged_profit_by_json()
    # _run_add_stg_2_account()
