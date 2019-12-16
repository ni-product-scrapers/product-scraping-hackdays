# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from .. items import ProductItem


class NicomSpider(CrawlSpider):
    name = 'nicom'
    allowed_domains = ['native-instruments.com']
    start_urls = tuple(['https://www.native-instruments.com/en/products'])

    def parse(self, response):
        print(response)
