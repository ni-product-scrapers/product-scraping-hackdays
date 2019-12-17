# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import re
from ..items import ProductItem


class MusikHausKornSpider(CrawlSpider):

    DOMAIN = 'musikhaus-korn.de'
    START_URL = 'https://www.musikhaus-korn.de/de/suche?q=native%20instruments&pagesize=24&sort=5&direction=1&style=1&f1=2$426'
    name = 'musikhauskorn'
    allowed_domains = [DOMAIN]
    start_urls = tuple([START_URL])

    def parse(self, response):
        products = response.xpath('//*[@id="search-product-list"]/div/div/div/a')
        for product in products:
            url = 'https://www.' + self.DOMAIN + product.xpath('@href').extract_first()
            print(url)
            item = ProductItem()
            item['shop'] = 'musikhauskorn'
            item['country'] = 'DE'
            item['product_url'] = url
            item['name'] = product.xpath('div[@class="name"]/text()').extract_first().strip()
            price_data = product.xpath('div[@class="price"]/text()').extract_first().split()
            item['price'] = price_data[0]
            item['currency'] = price_data[1]
            item['image_url'] = 'https:' + product.xpath('div[@class="image"]/img/@src').extract_first()

            yield item

        number_of_pages = response.xpath('//*[@id="pagination"]/ul/li').extract()
        for page_number in range(2, 5):
            link = '{}&page={}'.format(self.START_URL, page_number)
            yield scrapy.Request(link, self.parse)
