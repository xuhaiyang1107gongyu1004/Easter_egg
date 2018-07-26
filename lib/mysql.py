#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用于处理mysql数据存储相关内容

import pymysql
from traceback import *

from config import serverconfig as sconf

class mysql(object):
    '''

    '''
    __connect = sconf.mysql_connect

    def __init__(self):
        self.connect = pymysql.connect(**self.__connect)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def __sql(self):
        self.cursor.execute(self.sql, args=self.arges)
        # print(self.sql,self.arges)
        self.connect.commit()
        return self.cursor.rowcount

    def selectFetc(self):
        self.__sql()
        return self.cursor.fetchone()

    def selectFetcAll(self):
        self.__sql()
        dList = []
        # for d in self.cursor.fetchall():
        #     print(d)
        #     dList.append(d)
        return self.cursor.fetchall()

    def insert(self):
        # print(self.cursor.rownumber())
        return self.__sql()

    def update(self):
        return self.__sql()

    def delete(self):
        return self.__sql()

    def setArges(self, arges):
        '''这里用来构造SQL语句'''
        self.arges = arges

    def set_sql(self, sql, arges=None):
        self.sql = sql
        self.arges = arges


# class userForMysql(mysql):


def main():
    # 初始化查询语句,查询语句中只有值可以参数化。其他的内容在数据库中需要指定
    sql = "SELECT userid,username FROM user WHERE userid > %s;"
    arge = ("2",)
    user = mysql()
    user.set_sql(sql,arge)
    data = user.selectFetc()
    print(type(data),data)
    data2 = user.selectFetcAll()
    print(data2)


    # sql = "INSERT INTO user\
    # (username,\
    # passwd,\
    # money,\
    # jifen,\
    # usernick) \
    # VALUE (%s,%s,%s,%s,%s)"
    # arge = ("小红2","123456",10,10,"洪金宝2")
    # 创建查询对象
    # user = mysql()
    # 配置查询语句
    # user.set_sql(sql, arge)
    # data = user.insert()


    # 更新数据测试
    # data = user.update()

if __name__ == "__main__":
    main()