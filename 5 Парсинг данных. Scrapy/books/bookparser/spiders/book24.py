import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = [f'https://book24.ru/search/page-1/?q=%D1%80%D0%B5%D0%BB%D0%B8%D0%B3%D0%B8%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5']

    def parse(self, response):
        self.page = 0
        while self.page < 50:
            self.page += 1
            next_page = f'https://book24.ru/search/page-{self.page}/?q=%D1%80%D0%B5%D0%BB%D0%B8%D0%B3%D0%B8%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5'
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//article[@class='product-card']//a[@class='product-card__name smartLink']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_pars)

    def book_pars(self, response: HtmlResponse):
        book_title = response.xpath("//h1/text()").get()
        authors_name = book_title[0:book_title.find(':')]
        base_price = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get()
        discount_price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()
        book_rating = response.xpath("//span[@class='rating-widget__main-text']/text()").get()
        link = response.url
        yield BookparserItem(book_title=book_title,
                             authors_name=authors_name,
                             base_price=base_price,
                             discount_price=discount_price,
                             book_rating=book_rating,
                             link=link)
