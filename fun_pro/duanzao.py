#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/6/23 08:55
# @Author :huchao
# @E_mail :gmclqb@163.com
# @QQ : 九零九一三零零八三
# 功能描述： 锻造功能逻辑

from pymongo import MongoClient

from time import *
from traceback import *
import random as R

from lib.mongo import mongoConnet
from lib.User import User
from config.itemconfig import item
from config.user_lv import user_exp_lv


class DuanZaoMon(mongoConnet):
    def find(self, userid, cloum):
        '''查询锻造信息'''
        # 查询条件
        que = {
            'userid': userid,
        }
        # 查询语句
        return self.cour.find_one(que, {"_id": 0, cloum: 1})

    def update(self, userid, data):
        '''插入一条锻造信息'''
        quer = {
            "userid": userid,
        }
        insertData = {
            "userid": userid,
            "updateTime": time(),
        }
        self.cour.update_one(filter=quer, update={'$set': data, '$setOnInsert': insertData}, upsert=True)


def duanZao(user, key_type):
    '''
    锻造功能函数
    :param user 需要传递一个用户user对象或者是user的id属性

    :returns ores: 返回是用户矿石道具的数量：列表
            btnSta：返回用户锻造功能的锻造状态列表
    '''
    DZMon = DuanZaoMon()
    # 锻造在集合中的域名
    collo_DZ = "duanzao"
    keySta = {str(collo_DZ): {}}
    # 钥匙锻造耗时
    workKeyTime = 10

    # post 查询/锻造指定钥匙的锻造情况
    keySta = DZMon.find(user.getUserID(), collo_DZ)
    try:
        # 查询指定锻造为端在状态：
        key_id_sta = keySta[collo_DZ].get(key_type, False)
        print(keySta, "查询keyID指定的钥匙锻造状态", key_id_sta)
    except KeyError:
        # 用户第一次锻造钥匙
        keySta = {str(collo_DZ): {str(key_type): int(time())}}
        DZMon.update(userid=user.getUserID(), data=keySta)
        return getOreNum(user)
    except TypeError:
        # 用户当前锻造位第一次锻造钥匙
        keySta = {str(collo_DZ): {str(key_type): int(time())}}
        DZMon.update(userid=user.getUserID(), data=keySta)
        return getOreNum(user)

    if keySta[collo_DZ].get(key_type, False):
        if int(keySta[collo_DZ].get(key_type)) == 1:
            # 表示钥匙锻造位处于闲置状态可以进行进行钥匙锻造操作：
            keySta[collo_DZ].update({str(key_type): int(time())})
            user.userItemUpdate(*item.get(int(key_type)).get('item_DZ'))
            DZMon.update(userid=user.getUserID(), data=keySta)
        # if int(keySta['duanzao'].get(key_type)) + workKeyTime > int(time()):
        #     # 表示锻造钥匙尚未锻造成功
        #     pass
        elif int(time()) - int(keySta[collo_DZ].get(key_type)) > workKeyTime:
            # 表示钥匙已经锻造成功用户可以提取钥匙,
            # 给用户增加指定的钥匙道具，同时设置指定的钥匙锻造位的锻造状态值为空
            keySta[collo_DZ].update({str(key_type): 1})
            DZMon.update(userid=user.getUserID(), data=keySta)
            # 增加用户的钥匙道具
            user.userItemUpdate(itemid=int(key_type), num=int(R.random() * 10))

            ores, btnSta = getOreNum(user)
            return ores, btnSta
    else:
        # 用户第一次锻造此类型的钥匙
        # 准备用户锻造钥匙所需要的数据
        # DZStatu = {str(collo_DZ): {str(key_type): int(time())}}
        keySta[collo_DZ].update({str(key_type): int(time())})
        # 消耗锻造钥匙需要消耗的矿石
        try:
            user.userItemUpdate(*item.get(int(key_type)).get('item_DZ'))
        except:
            print_exc()
        # 更新用户的指定钥匙的锻造信息
        DZMon.update(userid=user.getUserID(), data=keySta)

    ores, btnSta = getOreNum(user)
    return ores, btnSta


def getOreNum(user):
    DZMon = DuanZaoMon()
    collo_DZ = 'duanzao'

    ores = dict()
    ore_list = [ore for ore in item.keys() if ore < 10100]
    # 准备矿石状态返回数据
    for oreId in ore_list:
        ores.update({oreId: user.getItem_num(itemid=oreId)})

    # 准备按钮状态返回状态
    key_type_dic = DZMon.find(userid=user.getUserID(), cloum=collo_DZ)
    print(key_type_dic)
    btnSta = dict()
    keylist = [keyid for keyid in item.keys() if keyid > 10100 and keyid < 10200]
    for keyid in keylist:
        try:
            if key_type_dic[collo_DZ][str(keyid)] > 1:
                btnSta.update({keyid: (True, key_type_dic[collo_DZ][str(keyid)] + 10 - int(time()))})
            else:
                btnSta.update({keyid: False})
        except KeyError:
            btnSta.update({keyid: False})
        except TypeError:
            btnSta.update({keyid: False})

    print(btnSta, ores)
    return ores, btnSta


if __name__ == "__main__":
    user = User(userid=2)
    print(duanZao(user, key_type=10101))

    # 查询 指定钥匙的是锻造情况
