# -*- coding: utf-8 -*-
import scrapy


class QuotesSimpleSpider(scrapy.Spider):
    name = 'quotes-simple'
    allowed_domains = ['toscrape.com']
    start_urls = (
        'http://quotes.toscrape.com/page/1/',
		'http://quotes.toscrape.com/page/2/',
    )

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }


class QuotesFilterTagSpider(scrapy.Spider):
    name = 'quotes-tag'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

class QuotesAuthorSpider(scrapy.Spider):
    name = 'quotes-author'
    allowed_domains = ['toscrape.com']
    start_urls = (
        'http://quotes.toscrape.com/',
    )

    def parse(self, response):
        for href in response.css('.author+a::attr(href)').extract():
            author_url = response.urljoin(href)
            yield scrapy.Request(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first().strip(),
            'birthdate': response.css('.author-born-date::text').extract_first().strip(),
            'bio': response.css('.author-description::text').extract_first().strip(),
        }

class QuotesXPathSpider(scrapy.Spider):
    name = 'quotes-xpath'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

