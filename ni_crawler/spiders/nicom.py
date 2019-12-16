# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ni_crawler.items import CrawlerItem

import json
import os
import re

import pdb




class NicomSpider(CrawlSpider):
    name = 'nicom'
    allowed_domains = ['native-instruments.com']
    start_urls = tuple(['https://www.native-instruments.com/en/products'])

    def parse(self, response):
        print(response)

