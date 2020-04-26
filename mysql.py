#-*-coding:utf-8 -*-
import pymysql
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import json

f = open(os.path.join(curPath, "config.js"), encoding="utf-8", errors='ignore')
config = json.load(f)
config = config[0]

class Mysql:

    # 进入数据库
    def __init__(self):
        host = config['database']['url']
        username = config['database']['username']
        password = config['database']['password']
        dbname = config['database']['dbname']
        database = pymysql.Connect(host=host, user=username, password=password, database=dbname, charset='utf8mb4')
        # 建立游标池
        self.db = database.cursor()

    # 执行查询
    def sql_result(self,sql):
        try:
            self.db.execute(sql)
            data = self.db.fetchall()
            return list(data)
        except Exception as e:
            raise e
        finally:
            self.db.close()

    # 查询结果转换
    def reslut_replace(self, sql):
        result = self.sql_result(sql)
        if result == []:
            result = ''
        else:
            result = result[0][0]
        return str(result)

    # 执行操作
    def do(self, sql):
        self.db.execute(sql)
        self.db.connection.commit()
        self.db.close()

