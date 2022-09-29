from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.db_books

    def process_item(self, item, spider):
        if item['base_price']:
            item['base_price'] = self.modification_price(item['base_price'])
        if item['discount_price']:
            item['discount_price'] = self.modification_price(item['discount_price'])
        if item['book_rating']:
            item['book_rating'] = self.modification_price(item['book_rating'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def modification_price(self, string):
        result = ''
        for i in string.replace('\xa0', '').replace(',', '.'):
            if i.endswith('₽'):
                continue
            result += i
        return float(result.strip())
