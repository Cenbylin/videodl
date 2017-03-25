#!/usr/local/bin/python
# encoding: utf-8
'''
任务获取器
@author: Cenbylin
'''
from db_access import VideoDB
import dl_config as cfg

#连接获得数据库实例
db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)

def get_job():
    pass

if __name__ == '__main__':
    a = {}
    a[str(123)] = 1
    a[str("123")] = 2
    print a[str(123)], a[str("123")]