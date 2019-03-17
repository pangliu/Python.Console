# -*- coding: utf-8 -*-
import os
import sys
import uuid
from datetime import datetime
from default_config import SqlConfig
import helper_dao as device_logs_dao

try:
    import mysql.connectorls
except:
    import mysql.connector

class SqlHelp:
    
    def __init__(self):
        self.db_connect = None

    def query_device_log(self, serial_no):
        self.connect_to_db()
        log = device_logs_dao.query_device_log_by_serial_no(
            self.db_connect, serial_no)
        # print(log)
        if log is not None:
            print('log is not none')
            return log
        else:
            print('log is none')

#--------------------------------------------------------------------------------------#
    # 以上為call dao專用 method
    # 以下為sql utils
#--------------------------------------------------------------------------------------#

    def connect_to_db(self):
        """連線SQL
        任何SQL動作前先call此Function
        """
        if self.db_connect is None:
            print('db_connect')
            self.db_connect = mysql.connector.connect(
                host=SqlConfig.HOST,
                user=SqlConfig.ACCOUNT,
                password=SqlConfig.PASSWORD,
                database=SqlConfig.DB_NAME)
                
    def close_db(self):
        """
        存取完DB需要關閉
        """
        self.db_connect.close
        self.db_connect = None