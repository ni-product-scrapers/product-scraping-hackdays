# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem


class NamePipeline(object):

    @staticmethod
    def process_item(self, item, spider):
        if item.get('name'):
            return item
        else:
            raise DropItem("Missing name in %s" % item)


