# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.CrawlSpider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )
    rules = (

    )

    def parse(self, response):
        pass
