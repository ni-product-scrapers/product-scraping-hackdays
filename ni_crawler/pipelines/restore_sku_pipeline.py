# -*- coding: utf-8 -*-

import json

import urllib2
from scrapy.exceptions import DropItem

RESTORE_ENDPOINT_URL = 'http://native-instruments.com/graphql'


class RestoreSkuPipeline(object):

    def process_item(self, item, spider):
        values = {
            'operationName': 'GetProductsForFinder',
            'variables': {
                'search': item['name'],
                'hitsPerPage': 1
            },
            'query': '''
                 query GetProductsForFinder(
                    $search: String
                    $language: Language
                    $hitsPerPage: Int
                  ) {
                    user(language: $language) {
                      getProducts(
                        search: $search
                        hitsPerPage: $hitsPerPage
                      ) {
                        result {
                          items {
                            id
                            title
                            sku
                          }
                        }
                      }
                    }
                  }
            '''
        }
        headers = {
            'Content-Type': 'application/json'
        }

        data = json.dumps(values)
        req = urllib2.Request(RESTORE_ENDPOINT_URL, data, headers)
        response = urllib2.urlopen(req, timeout=5)
        response_body = response.read()
        response = json.loads(response_body)

        try:
            restored_item = response['data']['user']['getProducts']['result']['items'][0]
            item['sku'] = restored_item['sku']

            # @deprecated. original name needs to be taken
            item['name'] = restored_item['title']
            return item
        except:
            raise DropItem('Could not find product in NI database: %s' % item)
