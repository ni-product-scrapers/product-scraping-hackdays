# -*- coding: utf-8 -*-
import scrapy
from .. items import ProductItem
from scrapy.spiders import CrawlSpider
import math


class Gear4MusicSpider(CrawlSpider):
    DOMAIN = 'gear4music.de'
    START_URL = 'https://www.gear4music.de/de/native-instruments?page=1'
    name = 'gear4music'
    allowed_domains = [DOMAIN]
    start_urls = tuple([START_URL])

    def parse(self, response):

        products = response.css('.g4m-grid-item.product-card')
        for product in products:
            url = 'https://www.' + self.DOMAIN + product.xpath('@href').extract_first()
            item = ProductItem()
            item['shop'] = 'gear4music'
            item['country'] = 'DE'
            item['product_url'] = url
            item['name'] = product.css('.product-card-title::text').extract()[0].strip()
            item['price'] = product.css('.product-card-price::text').extract()[0].split()[0]
            item['currency'] = product.css('.product-card-price::text').extract()[0].split()[1]
            item['image_url'] = url

            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_image_url)

        number_of_pages = math.ceil(int(response.css('body > div.single-column-responsive-layout.style-alt > div.container-fluid.plp-page.content.hide-on-search > div > div > div.widget--product-listing > div > div > div.react-product-listing-widget__message--listing-count > p > span::text')[1].extract()) / 45)
        for page_number in range(2, number_of_pages):
            link = '{}?page={}'.format(self.START_URL, page_number)
            yield scrapy.Request(link, self.parse)

    @staticmethod
    def parse_image_url(response):
        item = response.meta['item']
        item['image_url'] = response.css('[itemprop="image"]')[0].xpath('@src').extract()[0]

        yield item
