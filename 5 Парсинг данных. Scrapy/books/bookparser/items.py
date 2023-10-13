import scrapy


class BookparserItem(scrapy.Item):
    book_title = scrapy.Field()
    authors_name = scrapy.Field()
    base_price = scrapy.Field()
    discount_price = scrapy.Field()
    book_rating = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
