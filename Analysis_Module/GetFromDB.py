"""
author： flowerlake
time： 2019-08-19
description： 从MongoDB中抽取某个问题下的所有回答
"""

from pymongo import MongoClient
import logging, json, re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GetFromDB():

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        # 初始化连接的数据库
        self.db = self.client.Zhihu_QA

    def get_content(self):

        all_content = []
        content_file = open("data/content_file.txt", "w+", encoding="utf-8")

        # 这个根据抓取的id
        coll = self.db.problem_id_31430452
        try:
            search_item = coll.find()
            for item in search_item:
                # all_content.append({item["author"]["name"]: item["content"]})

                process_string = re.sub("<.*?>","",item["content"])
                process_string = re.sub("\n", "", process_string)
                content_file.write(process_string + "\n")
                all_content.append(process_string)
            logger.info("from {0} search success, search result type: {1}".format(coll,type(search_item)))
            # with open("data/analysis_text.json", "w+", encoding="utf-8") as f:
            #     json.dump(obj=all_content, fp=f)
        except Exception as e:
            logger.info(e)

        content_file.close()

        return all_content


if __name__ == "__main__":
    test = GetFromDB()
    answers = test.get_content()
