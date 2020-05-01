# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2019/2/24'
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
import time

import requests
import tushare as ts
import pandas as pd
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
from datetime import datetime
# from mpl_finance import candlestick_ochl
# import matplotlib.pyplot as plt

# from candlePlot import candlePlot
# from pyecharts import Kline
from pyecharts import Line
from sqlalchemy import create_engine

basic = './Data/stock_basic.csv'
company_basic = './Data/company_basic.csv'

token = '122caaa90d62e90b164ffdcb90d83cf19bc69d230216e50fb5f6d330'
ts.set_token(token)
pro = ts.pro_api()


# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')


def get_stock_basic():
    """
    获取股票列表数据接口
    :return:
    """
    for item in ['SSE', 'SZSE']:
        data = pro.stock_basic(exchange=item, list_status='L',
                               fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_status,delist_date,is_hs')
        # data = pro.stock_basic(exchange='SZSE,SSE', list_status='L')
        table = "stock_basic"
        # save_data_sql(data, table)
        data.to_csv("stock_info.csv",mode="a")


def get_index_basic():
    df = pro.index_basic(market='SSE')
    print(df.head())
    


def get_comp_basic_info():
    """
    获取上市公司基本信息
    :return:
    """
    table = 'stock_company'
    for item in ['SSE', 'SZSE']:
        df = pro.stock_company(exchange=item,
                               fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
        # df.to_csv(company_basic)

        save_data_sql(df, table)


def get_top_data():
    """
    获取龙虎榜数据
    :return:
    """
    df = pro.query('top_list', trade_date='20191101')
    print(df.head())
    # df.to_csv("top.csv")


def get_day_data(codes):
    table = "stock_day"
    for ts_code in codes:
        df = ts.pro_bar(ts_code=ts_code[0],adj='qfq',start_date='20010101',end_date='20131231')
        try:
            save_data_sql(df,table)
        except AttributeError as e:
            print("{}-无数据！".format(ts_code[0]))
            
            
def get_60_min(codes):
    table = "stock_60_minute"
    for ts_code in codes:
        df = ts.pro_bar(ts_code=ts_code[0], adj='qfq',freq='60min', start_date='20190101', end_date='20190531')
        try:
            save_data_sql(df, table)
            time.sleep(10)
        except AttributeError as e:
            print("{}-无数据！".format(ts_code[0]))
   
def get_trade_dates():
    df = pro.query('trade_cal', start_date='20050101', end_date='20190612')
    dates = df[['cal_date']].values.tolist()
    return dates


def get_lhb():
    table = "stock_lhb"
    dates = get_trade_dates()
    for date in dates:
        try:
            df = pro.top_list(trade_date=date[0])
            save_data_sql(df,table)
        except Exception as e:
            time.sleep(10)


def get_index():
    df = pro.index_daily(ts_code='000001.SH', start_date='20190101', end_date='20191231')
    return df


def read_stock_codes():
    df = pd.read_csv("stock_info.csv", engine='python', encoding='utf-8')
    codes = df[['ts_code']].values.tolist()
    return codes



def draw_index_kandle(data):
    # print(type(data.trade_date))
    # for date in data.trade_date:
    # print(type(date))
    del data['ts_code']  # 删除第一列
    del data['trade_date']
    # data.trade_date = [date2num(datetime.strptime(date,"%Y%m%d")) for date in data.trade_date]   # 将日期转为时间戳
    sh15list = []
    for i in range(len(data)):
        sh15list.append(data.iloc[i, :4])
    # print(sh15list)
    kline = Kline("K 线图示例")
    kline.add("日K", ["2019/03/{}".format(i + 1) for i in range(15)], sh15list)
    kline.render()
    # ax = plt.subplot()
    # mondays = WeekdayLocator(MONDAY)
    # weekFormatter = DateFormatter("%y %b %d")
    # ax.xaxis.set_major_locator(mondays)
    # ax.xaxis.set_major_locator(DayLocator())
    # ax.xaxis.set_major_formatter(weekFormatter)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # ax.set_title("上证综合指数")
    # candlestick_ochl(ax,sh15list,width=0.9,colorup='g',colordown='r')
    # plt.setp(plt.gca().get_xticklabels(),rotation=80,horizontalalignment='center')
    # plt.show()


def get_bonus():
    df = pro.dividend(ts_code='601398.SH', fields='ts_code,div_proc,stk_div,cash_div_tax,record_date,ex_date')
    df.to_csv("ICBC.csv")


def save_data_sql(df, table):
    engine = create_engine("mysql+pymysql://root:cyh187977@127.0.0.1:3306/spider?charset=utf8")
    df.to_sql(name=table, con=engine, if_exists='append', index=False, index_label=False)


def resample_df(df):
    date = df['trade_date']
    df.index = date
    print(df)
    df = df.resample("M").sum()
    print(df)
    
def calculate_change_percent(df):
    """
    计算涨跌幅
    :return:
    """
    df['tmp'] = df['close'].shift(1)
    df['change_percent'] = (df['tmp']-df['close'])/df['close']
    
def cnt_interval_change_percent_single(change_data):
    """
    涨跌幅区间统计-个股
    :return:
    """
    # todo
    pass

def cnt_interval_change_percent_index(change_data):
    """
    涨跌幅区间统计-大盘
    :param change_data:
    :return:
    """
    # todo
    pass


def get_fund_basic():
    """
    获取基金列表
    :return:
    """
    df = pro.fund_basic(market='E')
    print(df.head())
    
    
def show_index_plot():
    """
    绘制大盘的折线图
    :return:
    """
    data = get_index()['close'].values.tolist()[::-1]
    index = get_index()['trade_date'].values.tolist()[::-1]
    line = Line("折线图示例")
    line.add(
        "大盘指数",
        index,
        data,
    )
    line.render('index.html')


if __name__ == '__main__':
    # get_comp_basic_info()
    # get_top_data()
    # data = get_index()
    # calculate_change_percent(data)
    # save_data_sql(data,"stock_index")
    # draw_index_kandle(data)
    # get_stock_basic()
    # codes = read_stock_codes()
    
    # get_day_data(codes)
    # get_60_min(codes)
    # get_lhb()
    # get_top_data()
    # get_index_basic()
    # get_index()
    # get_fund_basic()
    show_index_plot()
