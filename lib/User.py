#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/5/24 22:15
# @Author :huchao

# 用户类
from time import *

from traceback import *
from pymysql import err

from lib import mysql
from lib import item_object
from config.user_lv import user_exp_lv


# from lib import mongo


class User(object):
    '''
    用户注册：
    如果self.state == 0 则用户处于未注册状态可以注册
    如果self.state !=0 则用户处于一注册状态，可以执行登录相关的操作
    '''

    def __init__(self, username=None, userid=None):
        '''初始化'''
        # 通过username字段初始化user对象
        if username:
            self.username = username
            self.msql = mysql.mysql()
            self.__getUserCreateUserid()
            if not self.userid:
                print("用户最初创建")
                self.createtime = self.logintim = ctime()
                return
            else:
                print(self.userid, "这里应该得到用户id")
                self.__getUserPasswd()
                self.uploadUserinfo()
        elif userid:
            self.userid = int(userid)
            self.msql = mysql.mysql()
            self.__getUsername()
            self.__getUserPasswd()
            self.__getUserPasswd()
            self.uploadUserinfo()

    def __del__(self):
        '''
        
        析构函数
        :return:
        '''

    def __call__(self):
        '''回调函数'''
        return self

    def setUserinfo(self, username, passwd, money, jifen, usernick, lv, exp_lv, **kwargs):
        '''新用户注册时，用来设置新用户信息'''
        self.username = username
        self.passwd = passwd
        self.money = money
        self.jifen = jifen
        self.usernick = usernick
        self.lv = lv
        self.exp_lv = exp_lv

    def setpasswd(self, passwd):
        '''设置用户的单项属性'''
        self.passwd = passwd

    def setUsernick(self, usernick):
        '''设置用户昵称'''
        self.usernick = usernick

    def setUsermoney(self, money):
        '''设置用户金钱'''
        self.money += money

    def setUserjifen(self, jifen):
        '''设置用户积分'''
        self.jifen += jifen

    def setUserlv(self):
        self.lv += 1

    def setUserExp_lv(self, exp_lv):
        self.exp_lv += exp_lv
        if self.exp_lv > user_exp_lv.get(self.lv):
            self.setUserlv()
        self.updateUserinfo()

    def getUserinfo(self):
        '''老用户登录时，用来拉取用户数据库信息'''
        self.uploadUserinfo()
        userinfo = {
            "userid": self.userid,
            "username": self.username,
            "passwd": self.passwd,
            "usernick": self.usernick,
            "money": self.money,
            "jifen": self.jifen,
            "lv": self.lv,
            "exp_lv": self.exp_lv
        }
        return userinfo

    def getUserID(self):
        '''
            获得用户ID
        '''
        return self.userid

    def getUserPasswd(self):
        '''获得用户密码'''
        return self.passwd

    def __getUserPasswd(self):
        '''拉取用户信息'''
        sql = "SELECT passwd FROM user WHERE username=%s;"
        self.msql.set_sql(sql, (self.username,))
        self.passwd, = self.msql.selectFetc()

    def __getUserCreateUserid(self):
        '''
        如果用户已经注册，返回该用户的userid
        如果用户未注册，返回False
        :return:
        '''
        sql = "SELECT userid FROM user WHERE username = %s;"
        self.msql.set_sql(sql, (self.username,))
        try:
            self.userid, = self.msql.selectFetc()
        except TypeError:
            self.userid = False

    def __getUsername(self):
        '''获得用户的username'''
        sql = "SELECT username FROM user WHERE userid=%s;"
        self.msql.set_sql(sql, (self.userid,))
        try:
            self.username = self.msql.selectFetc()
        except Exception:
            raise ValueError("userid不存在！userid非法！")

    def userItemUpdate(self, itemid, num):
        '''更新用户道具'''

        if int(itemid) < 1000:
            # 更新用户金币
            if itemid == 1:
                #更新金币
                self.setUsermoney(num)
            elif itemid == 2:
                #         更新积分
                self.setUserjifen(num)
            # 把更新后的用户信息写入数据库
            self.updateUserinfo()

        else:
            try:
                # 初始化用户所属道具对象
                print(self.userid, "这里初始化用户所属道具对象")
                self.item = item_object.Item(userid=self.userid, itemid=itemid)
                self.item.updateItem(num)
            except err.IntegrityError as e:
                print_exc()
                return 1, e
    def getItem_num(self, itemid):
        '''获得用户指定item的数量'''
        item = item_object.Item(userid=self.userid, itemid=itemid)
        itemInfo = item.get_itemInfo()
        return itemInfo.get("itemNum")

    def getItemInfo(self, itemid):
        '''获取用户指定的item信息'''
        item = item_object.Item(userid=self.userid, itemid=itemid)
        return item.get_itemInfo()

    def updateUserinfo(self):
        '''用于上传更新用户信息'''
        if self.userid == False:
            print("New user create")
            # 新用户注册
            sql = "INSERT INTO user(userid,username,passwd,money,jifen,usernick,lv,exp_lv) VALUE(%s,%s,%s,%s,%s,%s,%s,%s);"
            args = (None, self.username, self.passwd, self.money, self.jifen, self.usernick, self.lv, self.exp_lv)
            self.msql.set_sql(sql, args)
            try:
                self.msql.insert()
            except Exception:
                print_exc()
            # 初始化用户item数据，新用户注册用户注册初期没有userid，需要后使用时手动补上userID
            self.__getUserCreateUserid()
            # # 手动重新设置item对象的userid属性
            # self.item.userid = self.userid
            # 初始化用户的道具属性
            # self.item.createItem()
        elif self.userid > 0:
            # 老用户信息更新
            sql = "UPDATE user SET usernick=%s,passwd=%s,money=%s,jifen=%s,lv=%s,exp_lv=%s WHERE username=%s;"
            args = (self.usernick, self.passwd, self.money, self.jifen, self.lv, self.exp_lv, self.username)
            self.msql.set_sql(sql, args)
            try:
                self.msql.update()
            except Exception:
                print_exc()

    def uploadUserinfo(self):
        '''用户拉取用户信息'''
        if self.userid > 0:
            sql = "SELECT passwd,money,jifen,usernick,lv,exp_lv FROM user WHERE username = %s"
            self.msql.set_sql(sql, (self.username,))
            try:
                self.passwd, self.money, self.jifen, \
                self.usernick, self.lv, self.exp_lv = self.msql.selectFetc()
            except Exception:
                print_exc()


def createUser(userdata):
    '''函数用来演示新用户创建流程'''
    # 实例用户对象
    user = User(userdata.get("username"))
    # 判断用户是否已经注册
    if user.getUserID():
        print("用户已经注册。请重新登录")
        return
    # 上传用户属性，并且刷新数据库
    user.setUserinfo(**userdata)
    user.updateUserinfo()


def loginUser(userdata):
    '''函数用来演示老用户登录流程'''

    user = User(userdata.get("username"))
    if user.getUserID() == None:
        print("用户未注册：请注册")
        return
    print(user.getUserPasswd(), userdata.get("passwd"))
    if user.getUserPasswd() == userdata.get("passwd"):
        user.uploadUserinfo()
        userinfo = user.getUserinfo()
        print(userinfo)
        for d in userinfo:
            print(userinfo.get(d))


def senduser():
    user1date = {
        "username": "gmclqb@qq.cn",
        "itemid": 10001,
        "num1": 10
    }
    user = User(user1date.get("username"))
    user.uploadUserinfo()
    user.userItemUpdate(user1date.get("itemid"), user1date.get("num1"))


def main():
    userdata = {
        "username": "test1@qq.cn",
        "passwd": "123456",
        "money": 100,
        "jifen": 0,
        "usernick": "百魅音王",
        "cratetime": gmtime(),
        "logintime": gmtime(),
        "lv": 1,
        "exp_lv": 100,
    }
    # 新用户创建出测试
    createUser(userdata)

    # 用户登录测试
    loginUser(userdata)

    senduser()


if __name__ == "__main__":
    main()
