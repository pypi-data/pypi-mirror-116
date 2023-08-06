"""
@author  : MG
@Time    : 2021/7/12 9:10
@File    : backup.py
@contact : mmmaaaggg@163.com
@desc    : 用于对数据库表进行备份。
"""
import configparser
import logging
import os
import zipfile
from typing import Dict, List
import datetime
from tqdm import tqdm
from ibats_utils.transfer import date_2_str
from vnpy.trader.setting import get_settings


# get_settings

def backup_tables_2_zips(schema_table_names_dic: Dict[str, List[str]],
                         sql_output_cache_folder: str = "output",
                         zip_output_folder: str = "output",
                         mysqldump_file_path=r"c:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
                         mysqldump_user_name: str = None, mysqldump_password: str = None,
                         mysqldump_host: str = None, mysqldump_port: str = None,
                         ):
    """
    通过mysqldump对表进行逐表备份，输出到指定目录 sql_output_cache_folder
    zip最高压缩率算法压缩后，删除源文件。输出zip文件到指定目录 zip_output_folder/[schema]_[yyyy-dd-mm]/table_name.zip
    :param schema_table_names_dic: 数据库Schema：[table_name1, table_name2, ...] 字典
    :param sql_output_cache_folder: sql缓存目录
    :param zip_output_folder: zip输出的根目录
    :param mysqldump_file_path: 如果为空则默认使用系统命令。如果不为空则使用指定文件运行
    :param mysqldump_user_name: mysqldump 用户名
    :param mysqldump_password: mysqldump 密码
    :param mysqldump_host: mysqldump host
    :param mysqldump_port: mysqldump port
    :return:
    """
    logging.info("备份开始。")
    # logger = logging.getLogger(__name__)
    # TODO: logic
    # 动态生成 .mysql.cnf 文件内容，程序运行结束，删除该文件：
    # [mysqldump]
    # user="***"
    # password ="***"
    # host = 192.168.1.57
    # port = 3306
    # mysqldump 命令用法
    # "c:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" --defaults-file='.mysql.cnf' vnpy dbbardata > dump_dbbardata_9999.sql

    # 生成配置文件，最后删除
    cfg = configparser.ConfigParser()
    cfg.add_section('mysqldump')
    if mysqldump_user_name is None or mysqldump_password is None or mysqldump_host is None or mysqldump_port is None:
        database_dic = get_settings('database')
        cfg.set('mysqldump', 'user', database_dic['.user'])
        cfg.set('mysqldump', 'password', database_dic['.password'])
        cfg.set('mysqldump', 'host', database_dic['.host'])
        cfg.set('mysqldump', 'port', str(database_dic['.port']))
    else:
        cfg.set('mysqldump', 'user', mysqldump_user_name)
        cfg.set('mysqldump', 'password', mysqldump_password)
        cfg.set('mysqldump', 'host', mysqldump_host)
        cfg.set('mysqldump', 'port', mysqldump_port)
    cfg.write(open('.mysql.cnf', 'w'))

    # 设置环境变量
    os.environ['WORK_HOME'] = mysqldump_file_path

    # dump
    today_str = date_2_str(datetime.date.today())
    logging.info(f"有 {len(schema_table_names_dic)} schema 将被备份")
    for schema, table_name_list in schema_table_names_dic.items():
        # 配置路径，创建缓存目录
        cache_folder_path = os.path.join(sql_output_cache_folder, schema)
        os.makedirs(cache_folder_path, exist_ok=True)
        total = len(table_name_list)
        logging.info(f"{schema} 有 {total} 个表将被备份")
        for table_name in tqdm(table_name_list, total=total, desc=schema):
            # 缓存文件名称
            sql_output_cache_file = os.path.join(cache_folder_path, f'dump_{schema}_{table_name}.sql')
            # 直接用{mysqldump_file_path}会乱码，可能是因为路径中有空格，要添加环境变量，直接用mysqldump
            # os.system(f'{os.environ.get("WORKON_HOME")} --defaults-file=".mysql.cnf" control_center role > dump_role_9999.sql')
            # os.system(f'mysqldump --defaults-file=".mysql.cnf" control_center role > dump_role_9999.sql')
            cmd_code = os.system(
                f'mysqldump --defaults-file=".mysql.cnf" {schema} {table_name} > {sql_output_cache_file}')
            if cmd_code != 0:
                logging.error(f'{schema} 中的 {table_name} 表dump失败！')

    # 删除环境变量和配置文件
    del os.environ['WORK_HOME']
    os.unlink(".mysql.cnf")
    logging.info("备份结束，压缩开始。")
    # zip
    total_count = 0
    success_count = 0
    fail_count = 0
    zip_file_path_list = []
    for schema in schema_table_names_dic.keys():
        # cache folder path
        cache_folder_path = os.path.join(sql_output_cache_folder, schema)
        sql_cache_files_list = os.listdir(cache_folder_path)
        total_files = len(sql_cache_files_list)
        # zip folder path
        zip_folder_path = os.path.join(zip_output_folder, f"{schema}_{today_str}")
        os.makedirs(zip_folder_path, exist_ok=True)
        for num, sql_cache_file in enumerate(sql_cache_files_list, start=1):
            filename, file_type = os.path.splitext(sql_cache_file)

            if file_type == '.sql':
                sql_cache_file_path = os.path.join(cache_folder_path, sql_cache_file)
                zip_file_path = os.path.join(zip_folder_path, filename + '.zip')
                try:
                    logging.info(f'正在压缩...{zip_file_path}')
                    with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipped:
                        zipped.write(sql_cache_file_path)
                    total_count += 1
                    success_count += 1
                    logging.info(f'{num}/{total_files}) {zip_file_path} 完成了压缩，共成功 {success_count} 个')
                    os.unlink(sql_cache_file_path)
                    zip_file_path_list.append(zip_file_path)
                except Exception as e:
                    fail_count += 1
                    logging.error(f'{zip_file_path} 压缩失败！失败 {fail_count} 个。异常：{e}')

    zip_dir_files = '\n'.join(zip_file_path_list)
    logging.info(f"压缩结束。成功 {success_count} 个，失败 {fail_count} 个。zip目录列表：\n{zip_dir_files}")


def run_backup_tables_2_zips():
    schema_table_names_dic = {
        'vnpy': [
            "account_strategy_mapping",
            "dbbardata",
            "order_data_model",
            "position_daily_model",
            "position_status_model",
            "strategy_backtest_stats",
            "strategy_backtest_stats_archive",
            "strategy_info",
            "strategy_status",
            "symbols_info",
            "trade_data_model",
            "trade_date_model",
            "user_account_mapping",
            "wind_future_adj_factor",
        ],
    }
    backup_tables_2_zips(
        schema_table_names_dic,
        r'd:\temp\mysql_backup_cache',
        r'f:\mysql_backup')


if __name__ == "__main__":
    run_backup_tables_2_zips()
