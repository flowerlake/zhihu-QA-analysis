"""
author： flowerlake
time： 2019-08-17
description： mongoDB的连接，持久化存储
"""
import datetime

import pymongo, logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ToMongoDB():

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.Zhihu_QA
        # self.item = item

    def process(self,item):
        # 如果要修改 Zhihu_QA 中的collection，要在这里修改一下collection的名称
        coll = self.db.problem_id_332943436
        try:
            insert_id = coll.insert_one(item).inserted_id
            answer_id = item["id"]
            logger.info("answer id: {},insert id: {}".format(answer_id,insert_id))
        except Exception as e:
            logger.info(e)


if __name__ == "__main__":
    items = {"author": "Mike",
             "id": 740989453,
             "text": "My first blog post!",
             "tags": ["mongodb", "python", "pymongo"],
             "date": datetime.datetime.utcnow()}
    test = ToMongoDB()
    test.process(items)
