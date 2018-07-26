#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/5/25 15:20
# @Author :huchao

from traceback import *

import lib.mysql as mysql
from config import itemconfig as itconf


def item_chaxun(func):
    '''装饰器用于检查道具id是否存在'''

    def arwap(self, itemid, **kwargs):
        if self.itemcf.get(itemid):
            # 如果道具是一注册道具，则需要注册该item对象属性
            self.itemid = itemid
            sql = "SELECT item_num FROM item WHERE itemid=%s AND ownerid=%s"
            args = (self.itemid, self.userid)
            self.msql.set_sql(sql, arges=args)
            self.item_num = self.msql.selectFetc()[0]
            self.itemPrice = self.itemcf.get(self.itemid).get("item_price")
            self.itemMsg = self.itemcf.get(self.itemid).get("item_msg")
            self.itemHome = self.itemcf.get(self.itemid).get("item_home")
            self.itemPicId = self.itemcf.get(self.itemid).get("item_picID")
            self.itemName = self.itemcf.get(self.itemid).get("item_name")

            func(self, *args, **kwargs)
        else:
            raise ValueError("道具未定义")

    return arwap


class Item(object):
    '''
    道具类：

    '''

    itemcf = itconf.item

    def __init__(self, userid, itemid):
        if self.itemcf.get(int(itemid)):
            self.msql = mysql.mysql()
            self.userid = str(userid)
            self.itemid = int(itemid)
        else:
            raise ValueError("道具未定义")

    def __call__(self, *args, **kwargs):
        '''回调函数'''

    def __iter__(self):
        '''初始化迭代器'''

    def __next__(self):
        '''迭代器协议'''

    def __getItemID(self):
        '''检查用户是否拥有指定道具
            如果拥有返回对应道具的id
            否则返回None
        '''
        sql = "SELECT itemid FROM item WHERE itemid=%s AND ownerid=%s;"
        self.msql.set_sql(sql, arges=(self.itemid, self.userid))
        return self.msql.selectFetc()

    def __init_itmeInfo(self):
        sql = "SELECT item_num FROM item WHERE itemid=%s AND ownerid=%s"
        args = (self.itemid, self.userid)
        self.msql.set_sql(sql, arges=args)
        if self.msql.selectFetc():
            self.item_num = self.msql.selectFetc()[0]
        else:
            self.item_num = 0
        self.itemPrice = self.itemcf.get(self.itemid).get("item_price")
        self.itemMsg = self.itemcf.get(self.itemid).get("item_msg")
        self.itemHome = self.itemcf.get(self.itemid).get("item_home")
        self.itemPicId = self.itemcf.get(self.itemid).get("item_picID")
        self.itemName = self.itemcf.get(self.itemid).get("item_name")

    def __createItem(self):
        '''创建道具'''
        sql = "INSERT INTO item(id,itemid,ownerid,item_name,item_num) VALUE(NULL,%s,%s,%s,%s)"
        args = (self.itemid, self.userid, self.itemcf.get(self.itemid).get("item_name"), 0)
        self.msql.set_sql(sql, args)
        self.msql.insert()

    def updateItem(self, num):
        '''更新用户指定的道具数量
        如果用户之前没有获得此道具，则首先在数据库中创建此道具，然后在添加此道具的数量
        '''
        if not self.__getItemID():
            self.__createItem()
        sql = "UPDATE item SET item_num=%s WHERE itemid=%s AND ownerid=%s"
        # 初始化道具属性
        self.__init_itmeInfo()
        self.item_num += num
        args = (self.item_num, self.itemid, self.userid)
        self.msql.set_sql(sql, args)
        self.msql.update()

    def get_itemInfo(self):
        '''
        查询查询指定id的道具信息
        id是值道具在数据库表中的唯一ID信息
        '''
        self.__init_itmeInfo()
        iteminfo = {
            "itemName": self.itemName,
            "itemPicId": self.itemPicId,
            "itemMsg": self.itemMsg,
            "itemHome": self.itemHome,
            "itemId": self.itemid,
            "itemPrice": self.itemPrice,
            "itemNum": self.item_num,
            "itemOwnId": self.userid,
        }
        return iteminfo

    def get_itemNum(self):
        '''
        获取用户指定道具的数量
        :return: 如果拥有该道具则返回道具数量，如果为拥有该道具则返回None
        '''
        self.__init_itmeInfo()
        return self.item_num


class itemiter(object):
    '''item可迭代对象'''

    def __init__(self):
        ''''''

    def __iter__(self):
        '''初始化迭代器'''

    def __next__(self):
        '''迭代器协议'''


def createItemTest():
    '''用于演示创建item的使用方法'''
    userID = 1
    item = Item(userid=userID)
    try:
        item.createItem()
    except ValueError:
        print_exc()
    print("道具创建完成")


def getItemTest():
    '''用于演示拉取item信息'''


def main():
    '''测试主函数'''
    userID = 1
    item = Item(userid=userID, itemid=10001)
    try:
        item.updateItem(num=2)
        print(item.get_itemInfo())
    except:
        print_exc()


if __name__ == "__main__":
    main()
