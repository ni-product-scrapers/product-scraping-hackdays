# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    shop = scrapy.Field()
    name = scrapy.Field()
    source_id = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    country = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    sku = scrapy.Field()
