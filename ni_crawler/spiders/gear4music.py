# -*- coding: utf-8 -*-
import scrapy
from .. items import ProductItem
from scrapy.spiders import CrawlSpider

PRODUCT_PAGES = {
    'https://www.gear4music.de/de/Recording-and-Computer/Native-Instruments-Maschine-Mikro-MK3/2NUC': {
        'name': 'Maschine Mikro MK3',
        'id': 'MaschineMikroMK3',
        'sku': 'MASCHINEMikroMk3',
    },
}


class Gear4MusicSpider(CrawlSpider):
    name = 'gear4music'
    allowed_domains = ['gear4music.de']

    def start_requests(self):
        for url in PRODUCT_PAGES.keys():
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        url = response.url

        item = ProductItem()

        item['shop'] = 'gear4music'
        item['country'] = 'DE'
        item['product_url'] = url
        item['name'] = PRODUCT_PAGES[url]['name']

        price_block = response.css('.info-row-price')
        item['price'] = price_block.css('[itemprop="price"]')[0].xpath('@content')[0].extract()
        item['currency'] = price_block.css('[itemprop="priceCurrency"]')[0].xpath('@content')[0].extract()

        item['image_url'] = response.css('[itemprop="image"]')[0].xpath('@src')[0].extract()

        yield item
