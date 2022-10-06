# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrainingprojectItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    vacancies_name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
