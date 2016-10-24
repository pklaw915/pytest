import scrapy.cmdline

# quotos
#scrapy.cmdline.execute("scrapy crawl quotes-xpath -o output/quotes-xpath3.json".split())


# zhihu
scrapy.cmdline.execute("scrapy crawl zhihu-login -o output/zhihu-login.json".split())