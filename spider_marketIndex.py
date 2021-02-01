import scrapy
import datetime
import helper_functions as hf
import re
import time

start = time.time()

class IndexSpider(scrapy.Spider):

    # name of the spider, which will be referred in cronjob
    name = "index"
    start_urls = [
        "https://finance.yahoo.com"
    ]

    def parse(self, response):

        """This method is called to handle the response downloaded for each request made.
        The response parameter is an instance that holds the page css content from which
        we will be extracting helpful information like s&p, dow 30 and nasdaq index."""

        # The object index holds the css content for the scrape
        index = response.css("span.Trsdu\(0\.3s\)::text").getall()

        # following objects are regex pattern that extract numeric content from different
        # index droping the following symbols '% | ()'. These are to make ETL operations
        # easier.
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
""".format("spider_marketIndex", "index", "Success", duration))
