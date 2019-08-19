"""
author： flowerlake
time： 2019-08-19
description： 从MongoDB中抽取某个问题下的所有回答
"""

from pymongo import MongoClient


class GetFromDB():

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        # 初始化连接的数据库
        self.db = self.client.Zhihu_QA

    def process(self):
        pass