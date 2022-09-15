import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%80%D0%B5%D0%BB%D0%B8%D0%B3%D0%B8%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5/?stype=0&page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_pars)

    def book_pars(self, response: HtmlResponse):
        book_title = response.xpath("//h1/text()").get()
        authors_name = response.xpath("//a[@data-event-label='author']/text()").get()
        base_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        book_rating = response.xpath("//div[@id='rate']/text()").get()
        link = response.url
        yield BookparserItem(book_title=book_title,
                             authors_name=authors_name,
                             base_price=base_price,
                             discount_price=discount_price,
                             book_rating=book_rating,
                             link=link)
