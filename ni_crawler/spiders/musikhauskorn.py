# -*- coding: utf-8 -*-
import scrapy
from .. items import ProductItem
from scrapy.spiders import CrawlSpider

PRODUCT_PAGES = {
    'https://www.musikhaus-korn.de/de/native-instruments-maschine-mikro-mk3/pd/170627': {
        'name': 'Maschine Mikro MK3',
        'id': 'MaschineMikroMK3',
        'sku': 'MASCHINEMikroMk3',
    },
}


class MusicHausKornSpider(CrawlSpider):
    name = 'musichauskorn'
    allowed_domains = ['musichaus-korn.de']

    def start_requests(self):
        for url in PRODUCT_PAGES.keys():
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        url = response.url
        item = ProductItem()
        item['shop'] = 'musichauskorn'
        item['country'] = 'DE'
        item['product_url'] = url
        item['name'] = PRODUCT_PAGES[url]['name']
        item['price'] = response.xpath('//*[@id="product-price"]/p[1]/span[1]/font/font/text()').extract_first()
        item['currency'] = response.xpath('//*[@id="product-price"]/p[1]/span[2]/font/font/text()').extract_first()
        item['image_url'] = response.xpath('//*[@id="product-main-image"]/div/img/@src').extract_first()
        item['sku'] = PRODUCT_PAGES[url]['sku']

        yield item
