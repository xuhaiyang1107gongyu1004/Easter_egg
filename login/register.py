#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/5/26 17:30
# @Author :huchao

from lib.User import *
from lib.item_object import *


def register(user_name, user_passwd, user_passwd2, user_nick, *args, **kwargs):
    '''用户注册'''
    print(user_name, user_passwd, user_nick)
    if user_name == '' or user_name == None:
        # 用户名为空返回 1
        raise ValueError("用户名不能为空")

    if user_passwd == '' or user_passwd == None:
        raise ValueError("用户密码不能为空")

    if user_passwd2 == '' or user_passwd2 == None:
        raise ValueError("用户密码不能为空")

    if user_passwd2 != user_passwd:
        raise ValueError("两次输入的密码不一致")

    userdata = {
        "username": user_name,
        "passwd": user_passwd,
        "money": 10000,
        "jifen": 0,
        "usernick": user_nick,
        "cratetime": gmtime(),
        "logintime": gmtime(),
        "lv": 1,
        "exp_lv": 0,
    }
    # 实例用户对象
    user = User(userdata.get("username"))
    # 判断用户是否已经注册
    if user.getUserID():
        print("用户已经注册。请重新登录")
        raise ValueError("用户已注册")
    # 上传用户属性，并且刷新数据库
    user.setUserinfo(**userdata)
    user.updateUserinfo()


if __name__ == '__main__':
    register()
