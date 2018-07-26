#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/6/25 20:29
# @Author :huchao
# @E_mail :gmclqb@163.com
# @QQ : 九零九一三零零八三
# 功能描述：神秘宝箱功能

from traceback import *

from config.itemconfig import item
from config.box_config import box as boxlist
from lib import *

def box(user,boxid):
    '''
    用户开宝箱时随机返回给用户积分和道具。以及一部分金币
    :param user:
    :param boxid:要开启的宝箱id
    :return: 返回钥匙的道具，以及奖励信息字典
    '''
    giftlist = None
    keyNum = -1
    # if user.getItem_num(int(giftlist.get('key_id')))>0:
    # 开宝箱消耗的钥匙数量
    if not boxid:
        key_list = dict()
        for keyid in [keyid for keyid in item.keys() if keyid> 10100 and keyid < 10200]:
            key_list.update({str(keyid):user.getItem_num(keyid)})
        print(key_list)
        return key_list, giftlist
        # 生成box开启奖励

    try:
        giftlist = boxlist.get(boxid)
        if user.getItem_num(int(giftlist.get('key_id')))>0:
            user.userItemUpdate(int(giftlist.get('key_id')),keyNum)
            try:
                user.userItemUpdate(int(giftlist.get("Ore_Awa_Id")),int(giftlist.get("Ore_Awaid_Num")))
            except:
                print_exc()
            try:
                user.userItemUpdate(int(giftlist.get("Prop_Awaid_Id")),int(giftlist.get("Prop_AWaid_Num")))
            except:
                print_exc()  
            key_list = dict()
            for keyid in [keyid for keyid in item.keys() if keyid> 10100 and keyid < 10200]:
                key_list.update({str(keyid):user.getItem_num(keyid)})
            return key_list, get_gift_msg(giftlist)
        else:
            key_list = dict()
            for keyid in [keyid for keyid in item.keys() if keyid> 10100 and keyid < 10200]:
                key_list.update({str(keyid):user.getItem_num(keyid)})
            print(key_list)
            return key_list, get_gift_msg(giftlist)
            # 将用户奖励添加到数据库中
    except:
        raise TypeError('宝箱id错误')
        


def get_gift_msg(giftlist):
    # {'box-id': 'box-4',
    #  # 矿石奖励
    #  'Ore_Awaid_Id': '10004',
    #  'Ore_Awaid_Num': random.choice(l),
    #  # 道具奖励
    #  'Prop_Awaid_Id': '10204',
    #  'Prop_AWaid_Num': random.choice(l),
    #  # 消耗钥匙id
    #  'key_id': '10104'
    #  },
    print(giftlist)
    print(giftlist.get('Ore_Awaid_Id'))
    print(item.get(int(giftlist.get('Ore_Awaid_Id'))).get('item_name'))
    msg = '您获得了{}  {} 个 ！  您获得了 {}  {} 个 ！'.format(
        # 矿石奖励 道具名称
        item.get(int(giftlist.get('Ore_Awaid_Id'))).get('item_name'),
        # 矿石奖励 数量
        giftlist.get('Ore_Awaid_Num'),
        # 道具奖励 名称
        item.get(int(giftlist.get('Prop_Awaid_Id'))).get('item_name'),
        # 道具奖励 数量
        giftlist.get('Prop_AWaid_Num')
    )

    return msg