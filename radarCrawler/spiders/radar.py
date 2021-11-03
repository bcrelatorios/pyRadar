import scrapy


class RadarSpider(scrapy.Spider):
    name = 'radar'
    start_urls = ['www.zumgrafica.com.br']

    def parse(self, response):
        yield {
            "url": response.status
        }
