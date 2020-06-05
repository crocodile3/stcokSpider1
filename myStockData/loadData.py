# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2020/2/14'
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

import tushare as ts
import pandas as pd

class MyStockStore:
    def __init__(self):
        token = '122caaa90d62e90b164ffdcb90d83cf19bc69d230216e50fb5f6d330'
        ts.set_token(token)
        self.pro = ts.pro_api()
        
        
    def save_data_mysql(self,data,table):
        """
        将数据存到MySQL
        :param data:
        :param table:
        :return:
        """
        pass

    def get_trade_dates(self,start_date,end_date):
        """
        获取交易日历
        :param start_date:
        :param end_date:
        :return:
        """
        df = self.pro.query('trade_cal', start_date=start_date, end_date=end_date)
        dates = df[['cal_date']].values.tolist()
        return dates

    def get_comp_basic_info(self):
        """
        获取上市公司基本信息
        :return:
        """
        table = 'stock_company'
        for item in ['SSE', 'SZSE']:
            df = self.pro.stock_company(exchange=item,
                                   fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
            self.save_data_mysql(df, table)
            
    
    def get_day_data(self,codes):
        """
        获取每天数据
        :param codes:
        :return:
        """
        table = "stock_day"
        for ts_code in codes:
            df = ts.pro_bar(ts_code=ts_code[0], adj='qfq', start_date='20010101', end_date='20131231')
            try:
                self.save_data_mysql(df, table)
            except AttributeError as e:
                print("{}-无数据！".format(ts_code[0]))

    def get_min_data(self,codes):
        """
        获取分钟的数据
        :param codes:
        :return:
        """
        # 做判断你是获取30分钟的数据还是获取60分钟的数据
        table = "stock_60_minute"
        for ts_code in codes:
            df = ts.pro_bar(ts_code=ts_code[0], adj='qfq', freq='60min', start_date='20190101', end_date='20190531')
            try:
                self.save_data_mysql(df, table)
                time.sleep(10)
            except AttributeError as e:
                print("{}-无数据！".format(ts_code[0]))
                
    
    