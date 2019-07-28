"""
author： flowerlake
time： 2019-07-10
description： 这里采用的是splash，利用JavaScript脚本对翻页进行模拟，从而实现动态页面的数据爬取。
"""


# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash)                     
    splash:go(splash.args.url)        --打开页面
    splash:wait(2)                    --等待加载
    splash:runjs("window.scrollTo(0,document.body.scrollHeight)") --运行js代码
    splash:wait(20)                    --等待加载
    return splash:html()              --返回页面数据
end
'''


# window.scrollTo(0,document.body.scrollHeight);可以实现直接跳转到页面底部


class AnswerspiderSpider(scrapy.Spider):
    name = 'answerSpider'
    allowed_domains = ['zhihu.com']
    start_urls = ["https://www.zhihu.com/question/333741760"]

    def start_requests(self):
        splash_args = {
            'lua_source': lua_script
        }
        for url in self.start_urls:
            # yield scrapy.Request(url, self.parse_result)
            yield SplashRequest(url, callback=self.parse_result, cache_args=['lua_source'], endpoint='execute',
                                args=splash_args)

    def parse_result(self, response):
        logging.info(u'start crawl zhihu question')
        with open("test.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
        people_name = response.xpath(
            "//div[@class='List']/div/div/div[@class='List-item']/div/div/div/meta[1]/@content").extract()
        logging.info(people_name)

        # imgs = response.xpath('')
        # contents = response.xpath('')
        # vote_label = response.xpath('')


# limit最多一次为20
# api_url = "https://www.zhihu.com/api/v4/questions/333741760/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=50&platform=desktop&sort_by=default"


