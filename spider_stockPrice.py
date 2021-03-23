import scrapy
import datetime
import helper_functions as hf
import re
import time
from random import randint

start = time.time()

class IndexSpider(scrapy.Spider):

    # name of the spider
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

        """This method is called to handle the response downloaded for each request made.
        The response parameter is an instance that holds the page css content from which
        we will be extracting helpful information like stock price, change in price(delta &
        delta %) and top 3 news headlines related to that company."""

        # These objects index & name hold the css content for the scrape
        index = response.css('div.D\(ib\) span.Trsdu\(0\.3s\)::text').getall()
        time.sleep(randint(1,5))
        name = response.css('div.D\(ib\) h1.D\(ib\)::text').getall()

        # This object holds the regex pattern to perform ETL on scraped data
        delta_pattern = re.compile(r'([+-]+\d+\.\d+)(\s).?([+-]+\d+\.\d+).+')

        yield {
            'datetime'              : datetime.datetime.now().strftime("%Y-%m-%d %X"),
            'name'                  : name[0],
            'price'                 : index[9].replace(",",""),
            'delta_price'           : delta_pattern.sub(r'\1\2\3',index[10]).split(" ")[0],
            'delta_price_perc'      : delta_pattern.sub(r'\1\2\3',index[10]).split(" ")[1],
            'top_3_news'            : response.css('a.Fz\(18px\)::text')[-3:].getall(),
            'news_source'           : response.css('div.Fz\(11px\)::text')[-3:].getall(),
        }

end = time.time()
duration = end - start

# Send Slack notifications
hf.slack_msg("""
```
script: {}.py,
datafile: {}.jl,
status: {},
runtime: {}
```
""".format("spider_stockPrice", "stock_prices", "Success", duration))
