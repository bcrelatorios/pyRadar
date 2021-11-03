import scrapy
import csv

class RadarSpider(scrapy.Spider):
    name = 'radar'
    start_urls = []
    arquivo_aberto = open('/urls.csv', 'r') 
    urls =  csv.reader(arquivo_aberto,delimiter=',')
    for row in urls:
        start_urls.append(row[0])

    def parse(self, response):
        yield {
            "url": response.status
        }
