import pymongo
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb://scrapinghub:hackdays2019@ni-scraped-products-shard-00-00-njxbf.gcp.mongodb.net:27017,"
            "ni-scraped-products-shard-00-01-njxbf.gcp.mongodb.net:27017,"
            "ni-scraped-products-shard-00-02-njxbf.gcp.mongodb.net:27017/test?ssl=true&replicaSet=ni-scraped-products"
            "-shard-0&authSource=admin&retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            collection = self.client.get_database('scraped-products').get_collection('items')
            item_exists = collection.find_one_and_update({"sku": item['sku'], "shop": item['shop']},
                                                         {"$set": dict(item)}, upsert=True)
            print(item_exists)
            # collection.insert(dict(item))
        return item
