# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2019/3/23'
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import json
import time

from lxml.html import etree
import requests
import pymysql
from retry import retry
from DBUtils.PooledDB import PooledDB



#################----MySQL配置----#####################
MYSQL_HOST = "127.0.0.1"
MYSQL_DATABASE = "stock"
MYSQL_USER = "root"
MYSQL_PASSWORD = "cyh187977"
MYSQL_PORT = 3306
#################----MySQL配置----#####################


headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Referer":"https://xueqiu.com/u/7318086163",
"Origin":"https://xueqiu.com",
"Cookie":"aliyungf_tc=AQAAADvcgn2gkgEAIg2AJ2ILVB4beQie; acw_tc=2760824915911898371164000efdf8eb61418037d9b7137956c1cd8bbceaf8; Hm_lvt_1db88642e346389874251b5a1eded6e3=1591189838; device_id=24700f9f1986800ab4fcc880530dd0ed; remember=1; xq_a_token=9ae37869331b104a8235d7a93b7eddc5ed355021; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIwNDAwNjA4NTcsImlzcyI6InVjIiwiZXhwIjoxNTkzNzgxOTM2LCJjdG0iOjE1OTExODk5MzY4ODIsImNpZCI6ImQ5ZDBuNEFadXAifQ.J07U5v2fiQXZcshnymRxfUG1aWLStnZS86cILZpjUiZD1hQExVLBh6xqkYFRtV6Y70DPu6cjjphP5Q7PL6TnWxB452D6Vu41Eez8fOHO6dZS6RHJ3BaPkX0O8v-v118bxERejc1bZIxfy_GFPU-up6JnmUnWDdIGnybEU-BIe5_g6T76ViB6BdZC1Nbt61WUhRRHI9gyY_2rLbo3U1xWaCnsmpOV6rFrFwyD44BDIfpESo_amiG2T1aFYdgxJazCptES4ZHhB1nOaxtz2dy4M5C3z1-fIRSF1P_sZKhZE0-aQEA_dmP8C3oJqEMOLTPVLAEM9Rz_1BLmHYPRNELhmw; xqat=9ae37869331b104a8235d7a93b7eddc5ed355021; xq_r_token=d94acb14046c2ffb70b1a7db0c8cbc156e82a209; xq_is_login=1; u=2040060857; is_overseas=0; snbim_minify=true; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1591189962"}

@retry(tries=10,delay=1,backoff=2,max_delay=8)
def get_profit(group_id):
    # url = "https://xueqiu.com/cubes/quote.json?code=ZH786708,ZH1384584,ZH1367584"
    url = "https://xueqiu.com/cubes/quote.json?code={}".format(group_id)
    res = requests.get(url,headers=headers)
    data = json.loads(res.text)
    dic= data.get(group_id)
    del dic["closed_at"]
    del dic["badges_exist"]
    get_detail(group_id)
    save_data_mysql(dic,"group_profit")

@retry(tries=10,delay=1,backoff=2,max_delay=8)
def get_detail(id):
    url = "https://xueqiu.com/P/{}".format(id)
    res = requests.get(url=url,headers=headers)
    html = res.content.decode()
    tree = etree.HTML(html)
    divs = tree.xpath("//div[@class='weight-list']/div")
    for div in divs:
        class_name = div.xpath("./span[@class='segment-name']/text()")[0]
        class_weight = div.xpath("./span[@class='segment-weight weight']/text()")[0]
        stocks = div.xpath("./following-sibling::a[1]")
        for stock in stocks:
            stock_name = stock.xpath(".//div[@class='name']/text()")[0]
            price = stock.xpath(".//div[@class='price']/text()")[0]
            stock_weight = stock.xpath(".//span[@class='stock-weight weight']/text()")[0]
            group = dict(
                group_id = id,
                stock_name = stock_name,
                price = price,
                stock_weight = stock_weight.replace("%",""),
                class_name = class_name,
                class_weight = class_weight.replace("%","")
            )
            # print(class_name,class_weight,stock_name,price,stock_weight)
            save_data_mysql(group,"stock_group")

@retry(tries=10,delay=1,backoff=2,max_delay=8)
def get_group(userid):
    url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={}&pid=-24".format(userid)
    res = requests.get(url,headers=headers)
    dic = json.loads(res.text)
    groups = dic.get("data").get("stocks")
    for group in groups:
        group_id = group.get("symbol")
        group_name = group.get("name")
        print("获取{}组合的信息".format(group_name))
        get_profit(group_id)
        time.sleep(1)
        get_detail(group_id)
        time.sleep(1)
    
        
@retry(tries=10,delay=1,backoff=2,max_delay=8)
def get_collect(uid):
    url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?pid=-1&category=1&size=1000&uid={}".format(uid)
    res = requests.get(url,headers=headers)
    json_data = json.loads(res.text)
    stocks = json_data.get("data").get("stocks")
    for stock in stocks:
        stock["userid"] = uid
        creadted = stock.get("created")
        timeStamp = float(creadted / 1000)
        timeArray = time.localtime(timeStamp)
        creadted_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        stock["created"] = creadted_time
        save_data_mysql(stock,"collect")
    
    
def open_mysql():
    # pool = ConnectionPool(**config)
    # pool.connect()
    db = pymysql.connect(
        host=MYSQL_HOST,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        charset='utf8'
    )
    # cursor = pool.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    return db,cursor
    
    
def save_data_mysql(item,table):
    data = item
    print(item)
    keys = ",".join(data.keys())
    values = ",".join(['%s'] * len(data))
    sql = 'insert into %s (%s) values (%s)' % (table,keys,values)
    print("{}-插入数据完成".format(item))
    print(sql)
    db, cursor = open_mysql()
    try:
        
        cursor.execute(sql,tuple(data.values()))
        db.commit()
    except Exception as e :
        print(e)
    finally:
        cursor.close()
        db.close()


def login():
    """
    账号登陆
    :return:
    """
    pass
      
    
def get_users():
    url = "https://xueqiu.com/recommend/user/industry.json?id=106"
    # url = "https://xueqiu.com/statuses/original/show.json?user_id=7859098475"
    res = requests.get(url,headers=headers)
    dic = json.loads(res.text)
    print(dic)
    # dic = eval(res.text.replace("null","None").replace("true","True").replace("false","False"))
    industries = dic.get("list")
    # print(industries)
    for industry in industries:
        users = industry.get("users")
        for user in users:
            created = user.get("created_at")
            timeStamp = float(created / 1000)
            timeArray = time.localtime(timeStamp)
            creadted_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            user["created"] = creadted_time
            userinfo ={}
            userinfo["id"] = user.get("id")
            userinfo["screen_name"] = user.get("screen_name")
            userinfo["name"] = user.get("name")
            userinfo["province"] = user.get("province")
            userinfo["city"] = user.get("city")
            userinfo["location"] = user.get("location")
            userinfo["description"] = user.get("description")
            userinfo["url"] = user.get("url")
            userinfo["domain"] = user.get("domain")
            userinfo["gender"] = user.get("gender")
            userinfo["verified"] = user.get("verified")
            userinfo["created"] = user.get("created")
            userinfo["areaCode"] = user.get("areaCode")
            userinfo["type"] = user.get("type")
            userinfo["followers_count"] = user.get("followers_count")
            userinfo["friends_count"] = user.get("friends_count")
            # save_data_mysql(userinfo,"users")
            print(userinfo)
            # 根据userid获取组合
            print("准备获取{}的组合数据".format(user.get("screen_name")))
            # get_group(user.get("id"))
            # get_collect(user.get("id"))
            
        
            
            
if __name__ == '__main__':
    # 1 现获取用户
    get_users()
    # 2 获取用户的股票收藏表跟组合表
    # get_profit()
    # get_collect()