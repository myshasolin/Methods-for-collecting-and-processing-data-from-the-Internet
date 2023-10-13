import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

#sj = https://www.superjob.ru/vakansii/slesar.html?geo%5Bt%5D%5B0%5D=4&page=1

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

    start_urls = ['https://hh.ru/vacancies/slesar?page=0&hhtmFrom=vacancy_search_catalog']

    def parse(self, response):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, method='GET', callback=self.vacancy_pars)

    def vacancy_pars(self, response: HtmlResponse):
        company_name = response.xpath("//div[contains(@class, 'bloko-column_m-0 bloko-column_l-6')]//span[@data-qa='bloko-header-2']//text()").getall()
        vacancies_name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        _id = response.url
        yield JobparserItem(company_name=company_name, vacancies_name=vacancies_name, salary=salary, url=url, _id=_id)
