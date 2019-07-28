### zhihu-QA-analysis

这个库的目的是爬取知乎下的某一个问题的全部答案，并对所有的答案进行数据分析。

#### way- 1：通过scrapy的splash方式实现动态抓取（answerSpider）

方法的核心的页面下拉代码为：

```JavaScript
function main(splash)
    splash:go(splash.args.url)        --打开页面
    splash:wait(2)                    --等待加载
    splash:runjs("window.scrollTo(0,document.body.scrollHeight)") --运行js代码
    splash:wait(20)                    --等待加载
    return splash:html()              --返回页面数据
end
```


这种方式目前还存在一个问题，即页面下拉不能实现无限下拉，导致爬取的内容还只是初始页面的内容。（TODO:需要解决的是逻辑控制的问题）

#### way- 2：利用知乎提供的api进行爬取（answerApiSpider）

```Python
#limit最多一次为20，api_url如下
api_url = "https://www.zhihu.com/api/v4/questions/333741760/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=50&platform=desktop&sort_by=default"
```

#### scrapy的框架图

scrapy框架图及解析：https://docs.scrapy.org/en/latest/topics/architecture.html

![](https://scrapy-chs.readthedocs.io/zh_CN/0.24/_images/scrapy_architecture.png)


