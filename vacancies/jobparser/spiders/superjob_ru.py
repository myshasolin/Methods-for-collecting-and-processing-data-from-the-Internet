import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/slesar.html?geo%5Bt%5D%5B0%5D=4&page=1']

    def parse(self, response):
        next_page = response.xpath("//a[contains(@rel, 'next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, 'YrERR HyxLN')]/@href").getall()
        for link in links:
            yield response.follow(link, method='GET', callback=self.vacancy_pars)

    def vacancy_pars(self, response: HtmlResponse):
        company_name = response.xpath("//div[@class='_8zbxf _1CgVc _1bPAn uSWb8']//span/text()").get()
        vacancies_name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_4Gt5t _2nJZK']//text()").getall()
        url = response.url
        _id = response.url
        yield JobparserItem(company_name=company_name, vacancies_name=vacancies_name, salary=salary, url=url, _id=_id)


