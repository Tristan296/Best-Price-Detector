import scrapy

class AllSpider(scrapy.Spider):
    name = 'all'

    start_urls = ['https://www.rebelsport.com.au/']
    counter = 0
    def __init__(self):
        self.links=[]

    def parse(self, response):
        self.links.append(response.url)
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)
            counter+=1
    
    print(counter)