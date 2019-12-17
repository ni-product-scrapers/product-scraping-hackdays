# -*- coding: utf-8 -*-
import scrapy
from .. items import ProductItem
from scrapy.spiders import CrawlSpider

DOMAIN = 'thomann.de'
START_URL = 'https://www.thomann.de/intl/search.html?sw=native%20instruments&ls=100&filter=true&manufacturer%5B%5D=Native%20Instruments'


class ThomannSpider(CrawlSpider):
    name = 'thomann'
    allowed_domains = [DOMAIN]
    start_urls = tuple([START_URL])

    def parse(self, response):
        products = response.css('#resultsContainer  a.article-link.link::attr("href")').extract()
        for product_link in products:
                yield scrapy.Request(product_link, self.parse_product)

        last_page = response.css('.page .rs-btn')[-1].css('::text')[0].extract()
        for page_number in range(2, int(last_page)):
            link = '{}&pg={}'.format(START_URL, page_number)
            yield scrapy.Request(link, self.parse)

    def parse_product(self, response):
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
