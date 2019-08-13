"""
author： flowerlake
time： 2019-08-02
description： 这里采用的是知乎的api方式，利用知乎api直接获取结果，从而实现动态页面的数据爬取。
api_url: "https://www.zhihu.com/api/v4/questions/333741760/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=50&platform=desktop&sort_by=default"
more： 这个spider可以直接运行即可
"""

import logging, requests, json
import scrapy

start_urls = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit={}&offset={}&platform=desktop&sort_by=default"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


def get_answer_num(url, q_id, limit, offset):
    response = requests.get(url.format(q_id, limit, offset), headers=headers)
    response_text = eval(response.text)

    answer_num = response_text["paging"]["totals"]

    print(response_text)

    with open("../../data/result.json", 'w+', encoding='utf-8') as f:
        json.dump(response_text, f)

    logging.info("answer number: {}".format(answer_num))
    return answer_num


def crawl_answer(url, q_id, limit, offset):
    response = requests.get(url.format(q_id, limit, offset), headers=headers)
    response_text = eval(response.text)


def to_mongo(result_dict):
    pass


if __name__ == "__main__":
    question_id = "333741760"
    limit = 5
    init_offset = 0
    get_answer_num(start_urls, question_id, limit, init_offset)


# TODO: 现在通过这个api确实可以获得知乎上某个问题下的数据，考虑到每一个请求下都有下一个请求api，是否需要通过这个提取，还是说通过直接加offset的方式
# todo: 除此之外，想要通过这次的知乎api服务，把docker使用一次，尽量把这种方式能够作为一个服务提供出去。数据库使用可以使用MongoDB的方式直接进行存储，但具体的存储方式还要梳理一下。
