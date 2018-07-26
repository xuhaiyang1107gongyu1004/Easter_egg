#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/5/28 00:32
# @Author :huchao

# 用来存储服务器配置相关内容
mysql_connect = {
    "host": 'localhost',
    "port": 3306,
    "user": 'root',
    "passwd": '123456',
    "db": 'Easter_egg',
    "charset": 'utf8',
    # "cursorclass":pymysql.cursors.DictCursor,
}

# 用户缓存数据库配置
mongo_connect = {
    "host":"localhost",
    "port":27017,
    # 库名
    "db":"Easter_egg",
    # 集合名
    "col": "userinfo",
}
