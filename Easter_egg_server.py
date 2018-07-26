#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/5/16 18:51
# @Author :huchao

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app, make_response
import os
import json

from threading import Thread

from lib.mysql import *
from lib.User import User

# 加载功能模块
from login.register import register
from login.userlogin import UserLogin as Ulogin
from fun_pro.ks import playKS,get_monty_info
from fun_pro.duanzao import duanZao,getOreNum
from fun_pro.box import box as openbox
from fun_pro.shop import shop as shoping

# 加载配置文件
from config.user_lv import user_exp_lv
from config import app_config
from config import itemconfig
from config import box_config

CONFIG = "/config"
app = Flask(__name__)


# print(app.config)

def ErrorTest(func):
    def award(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AttributeError:
            return render_template("login.html")

    return award


@app.route("/")
def mian():
    '''主业务流程'''
    # 用来保存系统中已经登录的用户
    Userlist = {}
    while True:
        pass


@app.route("/register", methods=["GET", "POST"])
def create():
    '''
    用于接受新用户创建请求
    使用URL http://127.0.0.1:5000/create?user_name=gmclqb@127.com&user_passwd=123456&user_nick=青翼蝠王
    '''
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        di = {
            "user_name": request.form.get("username"),
            "user_passwd": request.form.get("userpasswd"),
            "user_passwd2": request.form.get("userpasswd2"),
            "user_nick": request.form.get("usernick"),
        }
        try:
            register(**di)
        except ValueError as e:
            # 用户注册失败
            return render_template("register.html")
        except TypeError as e:
            return render_template("register.html")

        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    '''

    :return:
    '''
    # 得到登录请求数据
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        di = {
            "get_user": request.form.get("username"),
            "get_pass": request.form.get("userpasswd"),
        }
        try:
            # 把当前用户信息存入全据变量中
            current_app.userdata = Ulogin(**di)
            # return render_template("main.html", **current_app.userdate, user_lv_exp=user_exp_lv)
            # 设置cookie。

            return redirect(url_for("monty"))
        except AttributeError as err:
            return render_template("login.html", username="用户名不存在")
        except ValueError as err:
            return render_template("login.html", pass_err=err)


@app.route("/KS", methods=["GET", "POST"])
def monty():
    '''矿山系统'''
    try:
        if request.method == "GET":
            montyData = get_monty_info(user=current_app.userdata)
            print(montyData)
            respo = render_template("firstPage.html", user=current_app.userdata,
                                    user_lv_exp=user_exp_lv,
                                    tool_sprit=tool_sprit_info(current_app.userdata),
                                    monty=montyData)

            return setCookie(respo)
        elif request.method == "POST":
            e = None
            di = dict()
            for i in request.form:
                di[i] = request.form.get(i)
            # 准备矿山数据
            try:
                montyInfo = playKS(**di, user=current_app.userdata, num=1)
            except ValueError as err:
                print_exc()
                montyInfo = get_monty_info(current_app.userdata)
                e = err
            except Exception:
                print_exc()
                return redirect(url_for('login'))
            # 准备 道具数据
            tool_sprit_info_list = tool_sprit_info(User(userid=request.cookies.get("userid")))
            respon = render_template("firstPage.html", user=current_app.userdata,
                                     tool_sprit=tool_sprit_info_list,
                                     user_lv_exp=user_exp_lv,
                                     monty=montyInfo,
                                     err = e)
            return setCookie(respon)
    except AttributeError:
        return redirect(url_for("login"))


def tool_sprit_info(user):
    '''函数用来获得用户的挖矿工具列表'''
    tool_sprit_list = [itemid for itemid in itemconfig.item.keys() if itemid > 10200 and itemid < 10300]
    tool_sprit_info_list = list()
    for item in tool_sprit_list:
        tool_sprit_info_list.append(user.getItemInfo(itemid=item))
    return tool_sprit_info_list


@app.route("/DZ", methods=["GET", "POST"])
def duanao():
    '''锻造系统'''
    key_id = [10101,10102,10103,10104,10105,10106]

    try:
        # 获得用户需要锻造的钥匙id
        if request.method == 'GET':
            ore ,btnSta = getOreNum(user=current_app.userdata)
            respon = render_template("duanzao.html", user=current_app.userdata,
                                     user_lv_exp=user_exp_lv,
                                     ore=ore,
                                     btnSta=btnSta,
                                     key_id=key_id)
            return setCookie(respon)

        elif request.method == 'POST':
            key_type = request.form.get('key_type',None)
            if not key_type:
                # 锻造的钥匙类型为空
                ore ,btnSta = getOreNum(current_app.userdata)
                errMsg = '锻造钥匙的类型为空'
                respon = render_template("duanzao.html", user=current_app.userdata,
                                         user_lv_exp=user_exp_lv,
                                         ore=ore,
                                         btnSta=btnSta,
                                         key_id=key_id,
                                         err=errMsg)
                return setCookie(respon)
            # 锻造的钥匙数据正常
            try:
                ore, btnSta = duanZao(user=current_app.userdata, key_type=key_type)
            except ValueError as err:
                ore,btnSta = get_monty_info(current_app.useudata)
                respon = render_template("duanzao.html", user=current_app.userdata,
                                         user_lv_exp=user_exp_lv,
                                         ore=ore,
                                         btnSta=btnSta,
                                         key_id=key_id,
                                         err=err)
                return setCookie(respon)

            respon = render_template("duanzao.html", user=current_app.userdata,
                                     user_lv_exp=user_exp_lv,
                                     ore=ore,
                                     btnSta=btnSta,
                                     key_id=key_id)
            return setCookie(respon)
    except AttributeError:
        return redirect(url_for("login"))


@app.route("/box", methods=["GET", "POST"])
def box():
    """宝箱系统"""
    try:
        if request.method == "POST":
            boxid = request.form.get('box')
        else:
            boxid = None
        print(boxid, '这里是宝箱的id')
        boxlist = ['box-1', 'box-2', 'box-3', 'box-4', 'box-5', 'box-6']
        keylist, giftlist = openbox(user=current_app.userdata, boxid=boxid)
        reps = render_template('box.html', user=current_app.userdata,
                               user_lv_exp=user_exp_lv,
                               boxid=boxlist,
                               keyNum=keylist,
                               err=giftlist)
        return setCookie(reps)
    except AttributeError:
        return redirect(url_for("login"))


@app.route("/send", methods=["POST", "GET"])
def send():
    '''交易大厅系统'''
    try:
        return render_template("exchange_home1.html", user=current_app.userdata,
                               user_lv_exp=user_exp_lv)
    except AttributeError:
        return redirect(url_for("login"))


@app.route("/PH")
def paihangbang():
    '''排行榜系统'''
    return "排行榜系统"


@app.route("/QD")
def qiandao():
    '''签到系统'''
    return "签到系统"


@ErrorTest
@app.route("/shop", methods=["GET", "POST"])
def shop():
    try:
        if request.method == "POST":
            msg = shoping(user=current_app.userdata, itemid=request.form.get('item'), num=1)
        else:
            msg = None
        resp = render_template("blacksStore.html", user=current_app.userdata,
                               user_lv_exp=user_exp_lv,
                               iteminfo=itemconfig.item,
                               err=msg)
        return setCookie(resp)
    except AttributeError:
        return redirect(url_for("login"))


@app.route("/DaiDing")
def daiding():
    return render_template("daiding.html")


@app.route("/test", methods=["GET"])
def test():
    return render_template("main.html")


def setCookie(rendTemp):
    '''函数用来设置cookie。和seesion，用来保存用户登录状态'''
    resp = make_response(rendTemp)
    resp.set_cookie("userid", str(current_app.userdata.getUserinfo().get("userid")))

    return resp


if __name__ == "__main__":
    app.config.from_object(app_config)
    app.run(host='0.0.0.0')
