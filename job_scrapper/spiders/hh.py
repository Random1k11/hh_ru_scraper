import scrapy

from job_scrapper.items import VacancyItem


class HhSpider(scrapy.Spider):
    name = "hh"
    main_url = 'https://hh.ru'

    def start_requests(self):
        urls = [
            'https://hh.ru/catalog/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categories_paths = response.xpath('//a[@class="catalog__item-link"]/@href').extract()
        for path in categories_paths:
            if path in ['/catalog/informacionnye-tehnologii-internet-telekom']:
                url = f'{self.main_url}{path}'
                yield scrapy.Request(url, callback=self.get_vacancies_urls)

    def get_vacancies_urls(self, response):
        vacancies_urls = response.xpath('//a[@class="bloko-link"]/@href').extract()
        for url in vacancies_urls:
            if 'feedback' not in url:
                yield scrapy.Request(url, callback=self.parse_vacancies)

    def parse_vacancies(self, response):
        title = response.xpath('//h1[@data-qa="vacancy-title"]//text()').extract_first()
        salary = ''.join(response.xpath('//p[@class="vacancy-salary"]//text()').extract()).replace(u'\xa0', u' ')
        company = ''.join(response.xpath('//a[@data-qa="vacancy-company-name"]//text()').extract())
        company_link = self.main_url + response.xpath('//a[@data-qa="vacancy-company-name"]/@href').extract_first()
        location = ''.join(response.xpath('//a[@data-qa="vacancy-view-link-location"]//text()').extract())
        employment_mode = response.xpath('//p[@data-qa="vacancy-view-employment-mode"]//text()').extract_first()
        description = ''.join(response.xpath('//div[@data-qa="vacancy-description"]//text()').extract())
        tags = response.xpath('//div[@class="bloko-tag-list"]//text()')
        if tags:
            tags = '; '.join(tags.extract())
        creation_time = ''.join(
            response.xpath('//p[@class="vacancy-creation-time"]//text()').extract()
        ).replace(u'\xa0', u' ')
        link = response.url

        item = VacancyItem()
        item['title'] = title
        item['salary'] = salary
        item['company'] = company
        item['company_link'] = company_link
        item['location'] = location
        item['employment_mode'] = employment_mode
        item['description'] = description
        item['tags'] = tags
        item['creation_time'] = creation_time
        item['link'] = link
        item['platform'] = 'hh.ru'
        yield item
