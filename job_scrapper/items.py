import scrapy


class VacancyItem(scrapy.Item):
    title = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    company_link = scrapy.Field()
    location = scrapy.Field()
    employment_mode = scrapy.Field()
    description = scrapy.Field()
    tags = scrapy.Field()
    creation_time = scrapy.Field()
    link = scrapy.Field()
    platform = scrapy.Field()
