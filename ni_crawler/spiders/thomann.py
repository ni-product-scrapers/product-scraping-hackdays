# -*- coding: utf-8 -*-
import scrapy
from .. items import ProductItem
from scrapy.spiders import CrawlSpider


PRODUCT_PAGES = ['https://www.thomann.de/intl/native_instruments_maschine_mikro_mk3.htm']


class ThomannSpider(CrawlSpider):
    name = 'thomann'
    allowed_domains = ['thomann.de']

    def start_requests(self):
        for url in PRODUCT_PAGES:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        url = response.url

        item = ProductItem()

        item['shop'] = 'thomann'
        item['country'] = 'DE'
        item['product_url'] = url

        item['name'] = response.css('[itemprop="name"]::text')[0].extract()

        price_block = response.css('.price-and-availability')
        item['price'] = price_block.css('[itemprop="price"]')[0].xpath('@content')[0].extract()
        item['currency'] = price_block.css('[itemprop="priceCurrency"]')[0].xpath('@content')[0].extract()

        item['image_url'] = response.css('.media-gallery img')[0].xpath('@src').extract()[0]

        yield item
