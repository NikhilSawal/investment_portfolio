import scrapy
import datetime
import helper_functions as hf
import re

hf.slack_msg("Start stock price scrape")

class IndexSpider(scrapy.Spider):
    name = "stock_price"
    start_urls = ['https://finance.yahoo.com/quote/TWLO?p=TWLO',
                  'https://finance.yahoo.com/quote/UAL?p=UAL',
                  'https://finance.yahoo.com/quote/ZNGA?p=ZNGA',
                  'https://finance.yahoo.com/quote/UBER?p=UBER',
                  'https://finance.yahoo.com/quote/CHGG?p=CHGG',
                  'https://finance.yahoo.com/quote/ETSY?p=ETSY',
                  'https://finance.yahoo.com/quote/GOCO?p=GOCO',
                  'https://finance.yahoo.com/quote/GOOGL?p=GOOGL',
                  'https://finance.yahoo.com/quote/CMG?p=CMG',
                  'https://finance.yahoo.com/quote/SHOP?p=SHOP',
                  'https://finance.yahoo.com/quote/TSLA?p=TSLA'
                  ]

    def parse(self, response):

        index = response.css('div.D\(ib\) span.Trsdu\(0\.3s\)::text').getall()
        name = response.css('div.D\(ib\) h1.D\(ib\)::text').getall()
        delta_pattern = re.compile(r'(.?\d+\.\d+)(\s).?(.?\d+\.\d+).+')

        yield {
            'datetime'   : datetime.datetime.now().strftime("%Y-%m-%d %X"),
            'name'       : name[0],
            'price'      : index[9].replace(",",""),
            'delta'      : delta_pattern.sub(r'\1\2\3',index[10]).split(" "),
            'top_3_news' : response.css('a.Fz\(18px\)::text')[-3:].getall(),
            'news_source': response.css('div.Fz\(11px\)::text')[-3:].getall(),
        }

hf.slack_msg("End stock price scrape")
