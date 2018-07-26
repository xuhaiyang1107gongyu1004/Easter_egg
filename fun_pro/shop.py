#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/6/26 19:11
# @Author :huchao
# @E_mail :gmclqb@163.com
# @QQ : 九零九一三零零八三
# 功能描述：


from traceback import *
from config.itemconfig import item
from lib import *



ItemList=[10201,10202,10203,10204,10205,10206]
def shop(user,itemid,num):
    '''
    购买商品
    查看金币
    金币是否可以购买相应的道具
    return:true,增加一个道具，减去相应的金币数目
    false,没有道具可以返回
    '''
    ItemMoney=0
    #更新金币
    flag=1
    #获取用户的金币数目
    print(ItemMoney,itemid,'金币书')
    ItemMoney=user.getUserinfo().get('money')
    item_price=item.get(int(itemid)).get('item_price')
    #金币数量不够，直接返回
    if ItemMoney <item_price:
        return "余额不足"
    #根据道具id，得到消耗的金币数，返回道具和剩下的金币
    if int(itemid) in ItemList:
        try:
            user.userItemUpdate(flag,-item_price)
            user.userItemUpdate(itemid,num)
            return '购买 {} 花费 {} 金币'.format(item.get(int(itemid)).get('item_name'),item_price)
        except Exception as e:
            print(e)
    else:
        print('id不存在') 
        return   '您购买的道具不存在'

       
   
        

    

    






