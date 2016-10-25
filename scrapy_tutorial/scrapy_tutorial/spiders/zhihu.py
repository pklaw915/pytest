# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy_tutorial.items import ZhihuItem


class ZhihuLoginSpider(CrawlSpider):
    name = 'zhihu-login'
    allowed_domains = ['zhihu.com''']
    start_urls = (
        'http://www.zhihu.com/',
    )
    rules = (
        Rule(LinkExtractor(allow=('/question/\d+#.*?', )), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=('/question/\d+', )), callback='parse_page', follow=True),
    )
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
        'Referer': 'http://www.zhihu.com/'
    }

    def start_requests(self):
        yield Request('https://www.zhihu.com', meta = {'cookiejar' : 1}, callback=self.post_login, headers=self.headers)

    def post_login(self, response):
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract_first()
        formdata = {
            '_xsrf': xsrf,
            'email': '123456',
            'password': '123456'
        }
        return FormRequest.from_response(response,
                                                meta={'cookiejar': response.meta['cookiejar']},
                                                headers=self.headers,
                                                formdata=formdata,
                                                callback=self.after_login,
                                                dont_filter=True,
        )

    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_page(self, response):
        yield {
            'url': response.url,
            'name': response.xpath('//span[@class="name"]/text()').extract(),
            'title': response.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract(),
            'description': response.xpath('//div[@class="zm-editable-content"]/text()').extract(),
            'answer': response.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract(),
        }
