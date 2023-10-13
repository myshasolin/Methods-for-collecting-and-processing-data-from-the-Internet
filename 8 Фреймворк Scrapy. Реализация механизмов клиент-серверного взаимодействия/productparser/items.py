# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
import re

class ProductparserItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    article = scrapy.Field()
    name = scrapy.Field()
    recommended_retail_price = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
    description = scrapy.Field()
    product_characteristics_keys = scrapy.Field()
    product_characteristics_values = scrapy.Field()
    product_characteristics = scrapy.Field()
