#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2018/5/27 23:55
# @Author :huchao


# 文件用来编写道具配置信息
# item ID 10001 ～ 10100属于矿石
# item ID 10101 ～ 10200属于钥匙
# item ID 10201 ～ 10300是矿锄道具
# 其他item号段暂时保留。后续有需要再行添加

item = {
    10001:{"itemid":10001,
           "item_name":"铁矿石",
           "item_msg":"这是铁矿石，找到铁匠后可以作为生产铁钥匙的原材料",
           "item_price":10,
           "item_picID":"铁矿石pciURL",
           "item_home":"黑石山"
           },
    10002:{"itemid":10002,
           "item_name":"铜矿石",
           "item_msg":"黑石山的矮人们只有运气好的时候才能偶尔采集到一点点铜矿石",
           "item_price":50,
           "item_picID":"铜矿石pciURL",
           "item_home":"黑石山"
           },
    10003:{"itemid":10003,
           "item_name":"银矿石",
           "item_msg":"为了采集银矿石经常矮人们常常会付出生命的代价",
           "item_price":100,
           "item_picID":"银矿石pciURL",
           "item_home":"黑石山"
           },
    10004:{"itemid":10004,
           "item_name":"金矿石",
           "item_msg":"金矿石已经不是普通的生命形态可以采集的矿石，常常需要向更高级的生命形态去兑换",
           "item_price":500,
           "item_picID":"金矿石pciURL",
           "item_home":"诸神芝山"
           },
    10005:{"itemid":10005,
           "itemc_name":"虚空矿石",
           "item_msg":"即使是诸神，采集虚空矿石也需要付出不菲的代价",
           "item_price":5000,
           "item_picID":"虚空矿石pciURL",
           "item_home":"诸神芝山"
           },
    10006:{"itemid":10006,
           "itemc_name":"老王矿石",
           "item_msg":"即使是诸神，采集虚空矿石也需要付出不菲的代价",
           "item_price":5000,
           "item_picID":"虚空矿石pciURL",
           "item_home":"诸神芝山"
           },

    #    以下是钥匙道具
    10101:{"itemid":10101,
           "item_name":"铁钥匙",
           "item_msg":"一级铁匠铺可以锻造铁钥匙",
           "item_price":500,
           "item_picID":"铁钥匙pciURL",
           "item_home":"诸神芝山",
           # 钥匙锻造消耗的矿石id,和数量
           'item_DZ':(10001,-1),
           },
    10102:{"itemid":10102,
           "item_name":"铜钥匙",
           "item_msg":"二级铁匠可以锻造童谣时候",
           "item_price":2000,
           "item_picID":"铜钥匙pciURL",
           "item_home":"诸神芝山",
           'item_DZ':(10002,-1),
           },
    10103:{"itemid":10103,
           "item_name":"银钥匙",
           "item_msg":"神才可以锻造银钥匙",
           "item_price":5000,
           "item_picID":"虚空矿石pciURL",
           "item_home":"诸神芝山",
           'item_DZ':(10003,-1),
           },
    10104:{"itemid":10104,
           "item_name":"金钥匙",
           "item_msg":"只有诸神中钻研锻造的大牛逼才能锻造金钥匙",
           "item_price":20000,
           "item_picID":"pciURL",
           "item_home":"诸神芝山",
           'item_DZ':(10004,-1),
           },
    10105:{"itemid":10105,
           "item_name":"虚空钥匙",
           "item_msg":"这恐怕只有系统大神才可以出门让我内心发颤",
           "item_price":5000,
           "item_picID":"虚空矿石pciURL",
           "item_home":"诸神芝山",
           'item_DZ':(10004,-1),
           },
    10106:{"itemid":10106,
           "item_name":"老王的钥匙",
           "item_msg":"这恐怕只有系统大神才可以出门让我内心发颤",
           "item_price":5000,
           "item_picID":"虚空矿石pciURL",
           "item_home":"诸神芝山",
           'item_DZ':(10004,-1),
           },

    #    以下是锄头道具
    10201:{"itemid":10201,
           "item_name":"铁锄头",
           "item_msg":"这就是一个普通的铁锄头",
           "item_price":50,
           "item_picID":"虚空矿石pciURL",
           "item_home":"铁匠铺或者商店都有卖"
           },
    10202:{"itemid":10202,
           "item_name":"狮子鎬",
           "item_msg":"这不是狮子做的镐头，是十字镐",
           "item_price":100,
           "item_picID":"虚空矿石pciURL",
           "item_home":"铁匠铺"
           },
    10203:{"itemid":10203,
           "item_name":"鹤嘴锄",
           "item_msg":"据说是一种形状很像仙鹤嘴巴的镐头。挖矿的效率很高",
           "item_price":200,
           "item_picID":"虚空矿石pciURL",
           "item_home":"这是铁匠铺老李头的镇店之宝"
           },
    10204:{"itemid":10204,
           "item_name":"一把锤子",
           "item_msg":"隔壁老张头爷爷的爷爷的爷爷传下来了，",
           "item_price":300,
           "item_picID":"虚空矿石pciURL",
           "item_home":"老张头家祖库"
           },
    10205:{"itemid":10205,
           "item_name":"牛逼的锤子",
           "item_msg":"隔壁老王就是用这把锤子破门的。一般人我不告诉他",
           "item_price":400,
           "item_picID":"虚空矿石pciURL",
           "item_home":"此锤只应天上有，人生哪个几回闻"
           },
    10206:{"itemid":10206,
           "item_name":"老王的锤子",
           "item_msg":"老王家的祖传锤子",
           "item_price":5000,
           "item_picID":"虚空矿石pciURL",
           "item_home":"此锤只应天上有，人生哪个几回闻"
           },
}