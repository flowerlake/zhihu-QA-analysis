"""
author： flowerlake
time： 2019-08-02
description： 这里采用的是知乎的api方式，利用知乎api直接获取结果，从而实现动态页面的数据爬取。
api_url: "https://www.zhihu.com/api/v4/questions/333741760/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=50&platform=desktop&sort_by=default"
more： 这个spider可以直接运行即可
"""

import logging, requests
import scrapy

question_id = "333741760"
limit = 5

start_urls = "https://www.zhihu.com/api/v4/questions/" + question_id + "/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit="+str(limit)+"&offset=0&platform=desktop&sort_by=default"

