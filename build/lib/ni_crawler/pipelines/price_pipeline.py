# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem


class PricePipeline(object):

    @staticmethod
    def process_item(self, item, spider):
        if item.get('price') and int(float(item.get('price'))) > 0 and item.get('currency'):
            return item
        else:
            raise DropItem("Missing price in %s" % item)


