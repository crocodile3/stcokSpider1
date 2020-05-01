# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2020/2/8'
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

# content = "测试信息"
# uids = "UID_TSfwkNQ65iBOgsmad7q3ttZ4y6C5"
# token = "AT_UgszzDw5cUjbISBpD2iUxCMmXpkEj13B"

# WxPusher.send_message(content, uids, token)
# WxPusher.query_message('<messageId>')
# WxPusher.create_qrcode('<extra>', '<validTime>', '<appToken>')
# WxPusher.query_user('<page>', '<page_size>', '<appToken>')
import json

import requests

from spider.render_test import tmp


class Pusher:
    def __init__(self):
        self.push_url = "http://wxpusher.zjiecode.com/api/send/message"
        self.uids = "UID_TSfwkNQ65iBOgsmad7q3ttZ4y6C5"
        self.token = "AT_UgszzDw5cUjbISBpD2iUxCMmXpkEj13B"
        self.body = {
          "appToken":self.token,
          "content":"这是一条测试信息",
          "contentType":1,
          "topicIds":[123],
          "uids":[self.uids]
        }
        
    def post(self,content_type,content):
        body = self.body
        body['content'] = content
        body['contentType'] = content_type
        try:
            res = requests.post(self.push_url,json=body)
            msg = json.loads(res.text)
            return msg
        except Exception as e:
            print("推送信息失败：{}".format(e))
            msg = {
                "code":1001,
                "msg" :"推送失败:{}".format(e)
            }
            return msg
        

if __name__ == '__main__':
    type = 2
    content = tmp
    pusher = Pusher()
    pusher.post(type,content)


