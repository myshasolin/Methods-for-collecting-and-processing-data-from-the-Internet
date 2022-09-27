# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import re
from datetime import datetime


class ProductparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.GALSER

    def process_item(self, item, spider):
        try:
            item['recommended_retail_price'] = int(''.join(re.findall('\d+', item['recommended_retail_price'])))
        except Exception as e:
            log_message = f"\n-----\nкосяк с ценой! {item['article']} - {item['name']} \n Описание ошибки {e}\n-----\n"
            print(log_message)
            pass
        try:
            item['product_characteristics'] = dict(zip(item['product_characteristics_keys'], item['product_characteristics_values']))
            del item['product_characteristics_keys'], item['product_characteristics_values']
        except Exception as e:
            log_message = f"\n-----\nкосяк с характеристиками! {item['article']} - {item['name']} \n Описание ошибки {e}\n-----\n"
            print(log_message)
            pass
        collection = self.mongo_base[item['category']]
        try:
            collection.insert_one(item)
            log_message = f"OK! товар арт. {item['article']} - {item['name']} добавлен в базу\n"
            print(log_message)
        except DuplicateKeyError:
            log_message = f"\n-----\nДУБЛЬ! информация о товаре арт. {item['article']} - {item['name']} обновлена\n-----\n"
            print(log_message)
            collection.replace_one({'_id': item['_id']}, item)
        with open('log_message.txt', 'a', encoding='UTF-8') as f:
            f.write(f'{datetime.now()} -- {log_message}')
        return item
