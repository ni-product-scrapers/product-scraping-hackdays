# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import validators


class ImageUrlPipeline(object):

    @staticmethod
    def process_item(self, item, spider):
        if item.get('image_url'):
            if validators.url(item.get('image_url')):
                return item
            else:
                raise DropItem("Not a valid url %s" % item)
        else:
            raise DropItem("Missing image url in %s" % item)


