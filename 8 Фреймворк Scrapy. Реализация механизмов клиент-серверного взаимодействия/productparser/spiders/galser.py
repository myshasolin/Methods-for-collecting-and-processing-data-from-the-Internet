import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from productparser.items import ProductparserItem
from scrapy.loader import ItemLoader
from dotenv import load_dotenv, find_dotenv
import os


class GalserSpider(scrapy.Spider):
    load_dotenv(find_dotenv())
    LOGIN = os.environ.get('login')
    PASSWORD = os.environ.get('password')

    name = 'galser'
    allowed_domains = ['galser.ru']
    start_urls = ['https://galser.ru/']
    galser_login_link = 'https://www.galser.ru/personal/'
    galser_login = LOGIN
    galser_password = PASSWORD

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.galser_login_link,
            method='POST',
            callback=self.login,
            formdata={
                'backurl': '/personal/',
                'AUTH_FORM': 'Y',
                'TYPE': 'AUTH',
                'USER_LOGIN': self.galser_login,
                'USER_PASSWORD': self.galser_password,
                'USER_REMEMBER': 'Y',
                'Login': 'Войти'
            }
        )

    def login(self, response: HtmlResponse):
        if response.text.find('Ваш персональный менеджер'):
            yield response.follow(
                '/catalog/',
                callback=self.categories_parsing
            )

    def categories_parsing(self, response: HtmlResponse):
        product_categories = response.xpath("//li/big/a/@href").getall()
        for category in product_categories:
            yield response.follow(
                category,
                self.product_parsing
            )

    def product_parsing(self, response: HtmlResponse):
        next_page = response.xpath("//a[@aria-label='Next page']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.product_parsing)
        links = response.xpath("//a[@class='catalog__item-image']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.good)

    def good(self, response: HtmlResponse):
        category = response.xpath("//span[@itemprop][last()]//nobr/text()").get()
        article = response.xpath("//span[@class='article-number']/text()").get()
        name = response.xpath("//h1/text()").get()
        recommended_retail_price = response.xpath("//span[@class='product__card-smallPrice']/text()").get()
        link = response.url
        _id = article
        description = ''.join(response.xpath(
            "//div[@class='product__card-inner2']//div[@class='product__card-descriptionText']/text()"
        ).getall()).replace('\n', '')
        product_characteristics_keys = response.xpath(
            "//div[@class='product__card-inner2']//tr/td[1]/text()"
        ).getall()
        product_characteristics_values = [el for el in ''.join(response.xpath(
            "//div[@class='product__card-inner2']//tr/td[2]//text()"
        ).getall()).replace('\t', '').replace('\n', '***').split(sep='***') if el != '']
        yield ProductparserItem(
            category=category,
            article=article,
            name=name,
            recommended_retail_price=recommended_retail_price,
            link=link,
            _id=_id,
            description=description,
            product_characteristics_keys=product_characteristics_keys,
            product_characteristics_values=product_characteristics_values
        )
