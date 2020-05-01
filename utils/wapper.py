# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2019/3/13'
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


def count_time(func):
    def wapper(num):
        start = time.time()
        func(num)
        end = time.time()
        print(end-start)
    return wapper
    
@count_time
def func(num):
    sum = 0
    for i in range(num):
        time.sleep(0.05)
        sum += 1
    print(sum)
    
func(10000)
        
        