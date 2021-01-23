import scrapy
import datetime
import helper_functions as hf

# Calls hf (helper function) to send notifications to slack
hf.slack_msg("Get company info")

class IndexSpider(scrapy.Spider):

    # name of the spider
    name = "company_profile"
    start_urls = ['https://finance.yahoo.com/quote/TWLO/profile?p=TWLO',
                  'https://finance.yahoo.com/quote/UAL/profile?p=UAL',
                  'https://finance.yahoo.com/quote/ZNGA/profile?p=ZNGA',
                  'https://finance.yahoo.com/quote/UBER/profile?p=UBER',
                  'https://finance.yahoo.com/quote/CHGG/profile?p=CHGG',
                  'https://finance.yahoo.com/quote/ETSY/profile?p=ETSY',
                  'https://finance.yahoo.com/quote/GOCO/profile?p=GOCO',
                  'https://finance.yahoo.com/quote/GOOGL/profile?p=GOOGL',
                  'https://finance.yahoo.com/quote/CMG/profile?p=CMG',
                  'https://finance.yahoo.com/quote/SHOP/profile?p=SHOP',
                  'https://finance.yahoo.com/quote/TSLA/profile?p=TSLA']

    def parse(self, response):

        """This method is called to handle the response downloaded for each request made.
        The response parameter is an instance that holds the page css content from which
        we will be extracting helpful information like name of company, sector to which the
        company belongs, industry and count of employees."""

        # These object (info & name) hold the css content for the scrape
        info = response.css('p.D\(ib\).Va\(t\) span.Fw\(600\)::text').getall()
        name = response.css('div.D\(ib\) h1.D\(ib\)::text').getall()

        yield {
            'datetime'       : datetime.datetime.now().strftime("%Y-%m-%d %X"),
            'name'           : name[0],
            'sector(s)'      : info[0],
            'industry'       : info[1],
            'employee_count' : response.css('span.Fw\(600\) span::text').get(),
        }

hf.slack_msg("Get company info DONE!!")
