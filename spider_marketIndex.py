import scrapy
import datetime
import helper_functions as hf
import re


hf.slack_msg("Start scrape")

class IndexSpider(scrapy.Spider):
    name = "index"
    start_urls = [
        "https://finance.yahoo.com"
    ]

    def parse(self, response):

        index = response.css("span.Trsdu\(0\.3s\)::text").getall()
        delta_pattern = re.compile(r'(.?\d+\.\d+)')
        delta_perc_pattern = re.compile(r'(.?\d+\.\d+).+')

        yield {
            'datetime'          : datetime.datetime.now().strftime("%Y-%m-%d %X"),
            's&p_500'           : index[0].replace(",",""),
            's&p_500_delta'     : delta_pattern.sub(r'\1', index[1]),
            's&p_500_delta(%)'  : delta_perc_pattern.sub(r'\1', index[2]),
            'dow_30'            : index[3].replace(",",""),
            'dow_30_delta'      : delta_pattern.sub(r'\1', index[4]),
            'dow_30_delta(%)'   : delta_perc_pattern.sub(r'\1', index[5]),
            'nasdaq'            : index[6].replace(",",""),
            'nasdaq_delta'      : delta_pattern.sub(r'\1', index[7]),
            'nasdaq_delta(%)'   : delta_perc_pattern.sub(r'\1', index[8]),
        }

hf.slack_msg("End scrape")
