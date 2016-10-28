import scrapy.cmdline

# quotes
#scrapy.cmdline.execute('scrapy crawl quotes-xpath -o output/quotes-xpath.json'.split())
scrapy.cmdline.execute('scrapy crawl quotes-author'.split())


# zhihu
#scrapy.cmdline.execute('scrapy crawl zhihu-login -o output/zhihu-login.json'.split())