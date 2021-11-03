import scrapy
import csv
import requests

class RadarSpider(scrapy.Spider):
    name = 'radar'
    start_urls = []
    r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSgpi7PovoovcZL28XpERljhBfOR_DFLlGNzwvlr2DyDn8-sBw9qvpfeh954TOm0eDZqBU_r8O0Bp5o/pub?gid=0&single=true&output=csv').text
    start_urls = r.split('\n')
    

    def parse(self, response):
        yield {
            "url": response.status
        }
