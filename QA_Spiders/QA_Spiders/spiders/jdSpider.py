# -*- coding: utf-8 -*-
import scrapy
# SplashRequest和scrapy.Request一样，我们这里用 SplashRequest替换scrapy.Request来实现JavaScript的加载
from scrapy_splash import SplashRequest

# document.getElementsByClassName('page')[0].scrollIntoView(true)
lua_script = '''
function main(splash)                     
    splash:go(splash.args.url)        --打开页面
    splash:wait(2)                    --等待加载
    splash:runjs("window.scrollTo(0,document.body.scrollHeight)") --运行js代码
    splash:wait(2)                    --等待加载
    return splash:html()              --返回页面数据
end
'''


class jdSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    # start_urls = ['http://jd.com/']
    keyword = 'python自营'  # 搜索的关键字
    base_url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format(keyword)

    def start_requests(self):
        '''重写start_requests'''
        yield scrapy.Request(self.base_url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        '''定义parse_urls执行splash元素'''

        # 获得商品总页数
        pageNum = int(response.css('span.fp-text>i::text').extract_first())

        # 构造每页的url，向Splash的execute端点发送请求
        for i in range(1):
            url = '{}&page={}'.format(self.base_url, 2 * i + 1)
            yield SplashRequest(url, endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'], callback=self.parse)

    def parse(self, response):
        '''解析页面'''

        # 获取一个页面中每本书的名字和价格等
        for sel in response.css('ul.gl-warp.clearfix > li.gl-item'):
            yield {
                'name': sel.css('div.p-name').xpath('string(.//em)').extract_first(),
                'price': sel.css('div.p-price i::text').extract_first(),
                'press': sel.css('span.p-bi-store a::text').extract_first(),
                'date': sel.css('span.p-bi-date::text').extract_first(),
            }
