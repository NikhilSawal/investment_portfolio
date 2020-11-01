import scrapy
import datetime

class IndexSpider(scrapy.Spider):
    name = "index"
    start_urls = [
        "https://finance.yahoo.com"
    ]

    def parse(self, response):
        index = response.css("span.Trsdu\(0\.3s\)::text").getall()
        yield {
            'datetime'          : datetime.datetime.now().strftime("%Y-%m-%d %X"),
            's&p_500'           : index[0],
            's&p_500_delta'     : index[1],
            's&p_500_delta(%)'  : index[2],
            'dow_30'            : index[3],
            'dow_30_delta'      : index[4],
            'dow_30_delta(%)'   : index[5],
            'nasdaq'            : index[6],
            'nasdaq_delta'      : index[7],
            'nasdaq_delta(%)'   : index[8],
        }
