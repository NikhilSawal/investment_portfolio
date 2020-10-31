import scrapy

class IndexSpider(scrapy.Spider):
    name = "index"
    start_urls = [
        "https://finance.yahoo.com"
    ]

    def parse(self, response):
        index = response.css("span.Trsdu\(0\.3s\)::text").getall()
        yield {
            's&p_500' : index[0],
            'dow_30'  : index[3],
            'nasdaq'  : index[6],
        }
