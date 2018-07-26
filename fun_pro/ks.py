#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/6/10 16:35
# @Author :huchao
# @E_mail :gmclqb@163.com
# @QQ : 九零九一三零零八三
# 功能描述：用来实现矿山功能。
# 矿山功能描述：用户通过挖矿功能，可以得到矿石道具。
# 用户挖矿条件判断。用户当前矿山未被开采，用户的铁锹的数量大于指定的数值。
# 用户矿山的挖掘状态存储在mongo缓存中。


from pymongo import MongoClient

from time import *
from traceback import *
import random as R

from lib.mongo import mongoConnet
from lib.User import User
from config.itemconfig import item
from config.user_lv import user_exp_lv

CLOUM = 'monty'

class Mongo(mongoConnet):
    '''类用来操作mongo 缓存。'''

    def find(self, userid, colum):
        '''
        用来查询指定域的值
        :param userid: 需要查询的用户id
        :param colum: 需要查询的字段
        :return: 如果查询的域的值存在，则返回改制
        '''
        query = {
            "userid": userid,
        }
        return self.cour.find_one(query, {"_id": 0, str(colum): 1})

    def update(self, userid, data):
        '''

        :param quer: 查询条件
        :param data: 需要更新的数据
        :return: 返回插入结果
        '''
        quer = {
            "userid": userid,
        }
        insertData = {
            "userid": userid,
            "updateTime": time(),
        }
        self.cour.update_one(filter=quer, update={"$set": data, "$setOnInsert": insertData}, upsert=True)


def playKS(user, monty=None, tool_sprit=None, num=1):
    '''用来执行挖矿操作
    monty : 矿山序号
    tool_sprit: 挖矿工具
    '''
    workTime = 10  # 当前挖矿完成时间未100秒
    userMon = Mongo()
    cloum = CLOUM

    # 查询指定的矿山是否处于挖矿状态
    montyStatu = userMon.find(user.getUserID(), cloum)
    try:
        monSta = int(montyStatu.get(cloum).get(str(monty)))
    except AttributeError:
        # 新用户第一次挖掘矿山
        print_exc()
        tool_sprit_num(user, tool_sprit, num)
        montyStatu = {"monty": {str(monty): int(time())}}
        userMon.update(userid=user.getUserID(), data=montyStatu)
        return userMon.find(user.getUserID(), colum=cloum)
    except TypeError:
        # 当前矿山id是第一次开采
        tool_sprit_num(user, tool_sprit, num)
        montyStatu[cloum].update({str(monty):int(time())})
        userMon.update(userid=user.getUserID(), data=montyStatu)
        return userMon.find(user.getUserID(), colum=cloum)
    try:
        if monSta == 0:
            # 如果指定矿山处于未开采状态，准备好挖矿数据进入挖矿状态
            # 检查用户的挖矿道具数量是否满足条件
            if not monty:
                raise ValueError('没有指定矿山无法挖掘矿山')
            if not tool_sprit:
                raise ValueError('矿山太硬了，没有锄头没有办法挖掘')
            if not num:
                raise ValueError('每次挖矿至少需要一把锄头')
            tool_sprit_num(user, tool_sprit, num)
            # 准备矿山数据
            montyStatu.get(cloum).update({str(monty): int(time())})
            # 消耗数量为num的采矿道具
            user.userItemUpdate(tool_sprit, -num)
            # 开始采矿
            userMon.update(userid=user.getUserID(), data=montyStatu)
            return get_monty_info(user)

        # 如果指定矿山处于挖掘完成状态
        elif int(time()) - monSta > workTime and monSta != 0:
            if not monty:
                raise ValueError('我必须知道您希望要提取哪座矿山的奖励')
            # 获得奖励列表
            award = getMontyItem()
            # 发放金币奖励
            user.userItemUpdate(1, award.get("gold"))
            # 发放积分奖励
            user.userItemUpdate(2, award.get("jifen"))
            # 发放矿石奖励
            for i in award.get("ore"):
                user.userItemUpdate(itemid=int(i[0]), num=int(i[1]))
            # 发放经验奖励：
            user.setUserExp_lv(award.get("exp"))
            # 重置矿山挖掘状态
            try:
                montyStatu.get(cloum)[str(monty)] = 0
                userMon.update(userid=user.getUserID(), data=montyStatu)
            except:
                print_exc()
                return get_monty_info(user)

    except TypeError as e:
        print_exc()
        # 如果用户当前矿山状态为未挖掘
        montyStatu.get(cloum).update({str(monty): int(time())})
        userMon.update(userid=user.getUserID(), data=montyStatu)
    except AttributeError as e:
        # 用户挖矿道具数量不足
        print_exc()
    except Exception as e:
        # 新用户第一次挖掘矿山
        print_exc()
        montyStatu = {str(cloum): {str(monty): int(time())}}
        userMon.update(userid=user.getUserID(), data=montyStatu)
    return userMon.find(user.getUserID(), colum=cloum)


def tool_sprit_num(user, tool_sprit, num):
    if int(user.getItem_num(itemid=tool_sprit)) < int(num):
        raise ValueError("矿锄数量不足，请到商城购买后再开采矿山！")
    else:
        user.userItemUpdate(itemid=int(tool_sprit), num=-int(num))


def get_monty_info(user):
    '''查询矿山开采状态'''
    cloum = CLOUM
    userMon = Mongo()
    try:
        montyinfo = userMon.find(user.getUserID(), colum=cloum)
        return montyinfo if montyinfo else {"monty": {"1": 0, "2": 0, "3": 0}}
    except AttributeError:
        return {"monty": {"1": 0, "2": 0, "3": 0}}


def getMontyItem():
    '''
    函数用来在用户达成挖矿条件后，生成奖励道具。
    奖励道具包含两种：一：1种矿石，二：一定数量的是金币,三：一定量的经验值
    :return:
    '''
    # 生成奖励的金币数量
    goldNum = int(R.random() * 100)
    jifenNum = int(R.random() * 30)
    exp = int(R.random() * 10)
    # 生成矿石随机池
    oreList = [ore for ore in item.keys() if ore > 10000 and ore < 10100]
    ore = R.sample(oreList, 1)
    awardOreList = list()
    for i in ore:
        awardOreList.append((i, int(R.random() * 5) + 1))
    award = {
        "gold": goldNum,
        "jifen": jifenNum,
        "ore": awardOreList,
        "exp": exp,
    }
    return award


if __name__ == "__main__":
    data = playKS(userid=2)
    print("这里是调用结果", data)
