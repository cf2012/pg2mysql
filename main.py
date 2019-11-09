#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import click
import mysql.connector
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def getenv(k:str) -> str:
    """ 读环境变量 """
    import os
    v = os.getenv(k)
    assert v is not None, f"Environment Variable {k} should not be None"
    return v


def copy(engine_src, sql: str, engine_dest, dest_table: str):
    # clear
    with engine_dest.connect() as conn:
        conn.execute(f"truncate table {dest_table}")

    with engine_src.connect() as conn:
        for df in pd.read_sql(sql, con=conn, chunksize=100000):
            df.to_sql(dest_table, engine_dest, if_exists="append",
                      index=False, chunksize=100000, method="multi")


@click.command()
@click.option('-f', '--config-file', required=True, help="配置文件名")
@click.option('-t', '--task',  multiple=True, required=True, help="要执行的同步任务,支持多个")
def main(config_file: str, task: tuple):
    """
    复制数据
    """
    click.echo(f"{config_file}, {task}")

    from configparser import ConfigParser
    config = ConfigParser()
    config.read_file(open(config_file, 'r', encoding="utf-8"))

    def _get(section, option, env_var):
        try:
            return config[section][option]
        except KeyError:
            print(config.sections())
            return getenv(env_var)

    db_conn_url_src = _get("common", "db_conn_url_src", "DB_CONN_URL_SRC")
    db_conn_url_dest = _get("common", "db_conn_url_dest", "DB_CONN_URL_DEST")

    engine_src = create_engine(db_conn_url_src)
    engine_dest = create_engine(db_conn_url_dest)

    for t in task:
        copy(engine_src, config[t]["export_sql"],
             engine_dest, config[t]["dest_table"])

    engine_src.dispose()
    engine_dest.dispose()


if __name__ == "__main__":
    main()
