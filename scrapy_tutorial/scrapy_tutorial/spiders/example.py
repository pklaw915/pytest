# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field
from scrapy.selector import Selector

class ExampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["dmoz.org"]
    start_urls = (
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    )

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        items = []
        for site in sites:
            item = ExampleItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
        return items
