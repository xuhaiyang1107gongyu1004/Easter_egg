#!usr/bin/env python3
# -*- coding:utf-8 -*-

from pymongo import MongoClient

from config.serverconfig import mongo_connect


class mongoConnet(object):
    '''简化mongo 使用小类'''
    __connect = mongo_connect

    def __init__(self):
        # 初始化mongo服务器配置
        self.connet = MongoClient(self.__connect.get("host"), self.__connect.get("port"))
        self.db = self.connet[self.__connect.get("db")]
        self.cour = self.db[self.__connect.get("col")]

    def ensure_collection(self):
        '''重写建表方法'''

    def find(self, userid, cloum):
        '''重写方法
            用来重写数据查询方法
        '''
        pass

    def insert(self, query):
        '''
        用来重写数据插入方法
        :return:
        '''
        pass

    def update(self, userid, data):
        '''用来重写数据更新防擦'''
        pass
