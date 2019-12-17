# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider

from ..items import ProductItem

DOMAIN = 'justmusic.de'
START_URL = 'https://www.justmusic.de/Article?Items=45&s=native%20instruments'


class JustMusicSpider(CrawlSpider):
    name = 'justmusic'
    allowed_domains = [DOMAIN]
    start_urls = tuple([START_URL])

    def parse(self, response):
        products = response.css('[data-id="Articles"] .title a::attr("href")').extract()
        for product_link in products:
            product_link_absolute = 'https://www.{0}{1}'.format(DOMAIN, product_link)
            yield scrapy.Request(product_link_absolute, self.parse_product)

        last_page = response.css('[data-id="Page"][data-page]:not(.active)')[-1].css('::attr("data-page")')[0].extract()
        for page_number in range(2, int(last_page)):
            link = '{}&Page={}'.format(START_URL, page_number)
            yield scrapy.Request(link, self.parse)

    def parse_product(self, response):
        url = response.url

        item = ProductItem()

        item['shop'] = 'justmusic'
        item['country'] = 'DE'
        item['product_url'] = url
        item['name'] = response.css('#article_navigation [itemprop="name"]::text')[0].extract()
        price_block = response.css('.custom_buybox')
        item['price'] = price_block.css('[itemprop="price"]')[0].xpath('@content')[0].extract()
        item['currency'] = price_block.css('[itemprop="priceCurrency"]')[0].xpath('@content')[0].extract()

        item['image_url'] = response.css('[itemprop="image"]')[0].xpath('@src').extract()[0]

        yield item
