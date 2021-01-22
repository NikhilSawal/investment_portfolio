import requests
import scrapy
import datetime
import helper_functions as hf


hf.slack_msg("Start scraping ip's")

class IndexSpider(scrapy.Spider):
    name = "ip_addreses"
    start_urls = [
        "https://free-proxy-list.net/"
    ]

    def parse(self, response):
        rows = response.css('table.table tr')
        for row in rows[1:-16]:
            entry = row.css('td::text').getall()
            yield {
                'ip_address'     : entry[0],
                'port'           : entry[1],
                'code'           : entry[2],
                'country'        : entry[3],
                'anonymity'      : entry[4],
                'google'         : entry[5],
                'https(%)'       : entry[6],
                'last_checked'   : entry[7],
            }

hf.slack_msg("End scraping ip's")
