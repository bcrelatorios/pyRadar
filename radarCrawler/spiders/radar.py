import scrapy
import csv
import requests
from bs4 import BeautifulSoup
class RadarSpider(scrapy.Spider):
    name = 'radar'
    start_urls = []
    r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSru6mdDPT9ZTvS8gteX0DX1yWy4WvtN8AqcJvfvUK72d-jKRo699y7Rvv3mjV55dBYYEXGV7nfRdys/pub?gid=0&single=true&output=csv').text
    start_urls = r.split('\n')
    

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)
    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        
        yield scrapy.Request(f'{response.url}sitemap.xml', callback=self.parse_sitemap, cb_kwargs=dict(main_url=response.url, status=response.status, certificate=response.certificate))
       
        # do something useful here...

    def parse_sitemap(self, response, main_url, status, certificate):
        
        bs = BeautifulSoup(response.body, 'html.parser')
        big = bs.find_all('loc')
        if len(big) >= 3:
            big = 'com big'
        else:
            big = 'sem big'
        yield {
            "url": main_url,
            "status": status,
            'big': big,
            'certificate': certificate,
        }

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            
            yield {
                'url': response.url,
                'status': response.status,
                'big': '',
                'certificate': response.certificate,
                
            }

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
           
            yield {
                'url': request.url,
                'status': 'DNSLookupError',
                'big': '',
                'certificate': '',
            }

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            
            yield {
                'url': request.url,
                'status': 'TimeoutError',
                'big': '',
                'certificate': '',
            }
