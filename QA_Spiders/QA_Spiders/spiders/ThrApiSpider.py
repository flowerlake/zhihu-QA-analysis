"""
author： flowerlake
time： 2019-08-02
description： 这里采用的是知乎的api方式，利用知乎api直接获取结果，从而实现动态页面的数据爬取。
api_url: "https://www.zhihu.com/api/v4/questions/333741760/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=50&platform=desktop&sort_by=default"
more： 这个spider可以直接运行即可
"""

import logging, requests, json
from time import sleep

import scrapy

from QA_Spiders.QA_Spiders.ToMongoDB import ToMongoDB

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

start_url = "https://www.zhihu.com/api/v4/questions/{q_i}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit={limit}&offset={offset}&platform=desktop&sort_by=default"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


def get_answer_num(url, q_id, _limit, offset):
    response = requests.get(url.format(q_i=q_id, limit=_limit, offset=offset), headers=headers)

    logger.info("init url: {}".format(url.format(q_i=q_id, limit=_limit, offset=offset)))

    logger.info("response status code {}".format(response.status_code))
    if response.status_code == 200:
        # Attention: 一开始通过eval来将string类型的文本加载成字典，但是在这里不知道为什么不可以，报错如下：
        # Error：NameError: name 'false' is not defined
        # Solved：saw yet another problem today pointed out by SilentGhost: eval doesn't handle true -> True, false -> False, null -> None correctly.
        # Solved：Kiv -- https://stackoverflow.com/questions/1083250/running-json-through-pythons-eval
        response_text = json.loads(response.text)
        logger.info("response type ".format(type(response_text)))
        answer_num = response_text["paging"]["totals"]

    logger.info("the answer number of this question: {answer_num}".format(answer_num=answer_num))
    return answer_num


def crawl_answer(url, q_id, _limit, a_number, client):
    """
    :param client: mongodb client instance
    :param url: 这个是构造的api_url
    :param q_id: 这个是问题的id号
    :param _limit: 每个api_url每一次请求的个数
    :param a_number: 总共的回答数量
    :return:
    """

    answer_file = open("../../data/result.json", 'a+', encoding='utf-8')

    # 在python中 // 表示整除
    for index in range(a_number // _limit + 1):
        offset = index * _limit
        try:
            response = requests.get(url.format(q_i=q_id, offset=offset, limit=_limit), headers=headers)
            logger.info("crawl page is {off},the url is {u}".format(off=offset, u=url))
            response_text = json.loads(response.text)
            res_data = response_text["data"]

            # write every answer item to mongo database
            for a_item in res_data:
                try:
                    assert type(a_item) == dict
                except AssertionError as e:
                    logger.exception(e)
                    # dict(a_item)
                client.process(a_item)

            # 这里两句话是把请求得到的数据存到文件中
            # answer_file.write(response.text)
            # answer_file.write("\n")

        except Exception as e:
            logger.exception("api url response exception is ".format(e))
        sleep(3)


if __name__ == "__main__":
    question_id = "31430452"
    limit = 20
    init_offset = 0
    answer_num = get_answer_num(start_url, question_id, limit, init_offset)

    MonClient = ToMongoDB()
    crawl_answer(start_url, question_id, limit, answer_num, MonClient)

# Solved: 现在通过这个api确实可以获得知乎上某个问题下的数据，考虑到每一个请求下都有下一个请求api，是否需要通过这个提取，还是说通过直接加offset的方式
# todo: 除此之外，想要通过这次的知乎api服务，把docker使用一次，尽量把这种方式能够作为一个服务提供出去。数据库使用可以使用MongoDB的方式直接进行存储，但具体的存储方式还要梳理一下。
# ToDo: 添加代理，还有将日志写到文件中去

