# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider

from ..items import ProductItem


PRODUCT_PAGES = ['https://www.musikhaus-korn.de/de/native-instruments-maschine-mikro-mk3/pd/170627']


class MusikHausKornSpider(CrawlSpider):
    name = 'musikhauskorn'
    allowed_domains = ['musikhaus-korn.de']

    def start_requests(self):
        for url in PRODUCT_PAGES:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        url = response.url
        item = ProductItem()
        item['shop'] = 'musikhauskorn'
        item['country'] = 'DE'
        item['product_url'] = url
        item['name'] = response.css('#product > h1::text')[0].extract()
        item['price'] = response.xpath('//*[@id="product-price"]/p[1]/span[1]/text()')[0].extract().replace(',', '.')
        item['currency'] = response.xpath('//*[@id="product-price"]/p[1]/span[2]/text()')[0].extract()
        item['image_url'] = response.xpath('//*[@id="product-main-image"]/div/img/@src').extract_first()

        yield item
