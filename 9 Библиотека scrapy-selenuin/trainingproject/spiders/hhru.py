import scrapy
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest
from trainingproject.items import TrainingprojectItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    page, total_pages, last_page = 0, -2, None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://hh.ru/vacancies/{kwargs.get('search')}?page=0&hhtmFrom=vacancy_search_catalog"]

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        while self.page != self.total_pages+1:
            urls = f'https://hh.ru/vacancies/analitik-big-data?page={self.page}&hhtmFrom=vacancy_search_catalog'
            self.start_urls.append(urls)
            self.page += 1
            yield SeleniumRequest(url=urls)

    def parse(self, response: HtmlResponse):
        if response.xpath("//div[@data-qa='pager-block']").get():
            self.last_page = self.total_pages
            self.total_pages = response.xpath("//a[@data-qa='pager-next']/../span[last()]/a/span/text()").get()
            if self.total_pages:
                self.total_pages = int(self.total_pages)
            else:
                self.total_pages = self.last_page+1
        else:
            self.total_pages = 0

        vacancies_links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_pars,)

    def vacancy_pars(self, response: HtmlResponse):
        company_name = response.xpath(
            "//div[contains(@class, 'bloko-column_m-0 bloko-column_l-6')]//span[@data-qa='bloko-header-2']//text()"
        ).getall()
        if not company_name:
            company_name = response.xpath("//span[@data-qa='bloko-header-2']//text()").getall()
        vacancies_name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        _id = response.url
        yield TrainingprojectItem(company_name=company_name,
                                  vacancies_name=vacancies_name,
                                  salary=salary,
                                  url=url,
                                  _id=_id)

    # # а если "напрямую", то вот:
    # def parse(self, response: HtmlResponse):
    #     for url in self.start_urls:
    #         yield SeleniumRequest(
    #             url=url,
    #             callback=self.parse_result,
    #             wait_time=10,
    #             wait_until=EC.element_to_be_clickable((By.XPATH, "//a[@data-qa='pager-next']"))
    #         )
    #
    # def parse_result(self, response: HtmlResponse):
    #     vacancies_links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
    #     for link in vacancies_links:
    #         yield response.follow(link, callback=self.vacancy_pars)
    #
    # def vacancy_pars(self, response: HtmlResponse):
    #     company_name = response.xpath(
    #         "//div[contains(@class, 'bloko-column_m-0 bloko-column_l-6')]//span[@data-qa='bloko-header-2']//text()"
    #     ).getall()
    #     vacancies_name = response.xpath("//h1/text()").get()
    #     salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
    #     url = response.url
    #     _id = response.url
    #     yield TrainingprojectItem(company_name=company_name,
    #                               vacancies_name=vacancies_name,
    #                               salary=salary,
    #                               url=url,
    #                               _id=_id)
