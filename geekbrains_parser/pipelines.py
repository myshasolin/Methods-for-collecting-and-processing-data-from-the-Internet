from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GeekbrainsParserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.GeekBrains

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
            print(f"Запись о специальности {item['name']} добавлена")
        except DuplicateKeyError:
            collection.replace_one({'_id': item['_id']}, item)
            print(f"Дубль! Запись о специальности {item['name']} обновлена")
        return item
