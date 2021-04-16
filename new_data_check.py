import json
import json_lines
from datetime import datetime
import helper_functions as hf

def data_check(file_name):

    '''
    This piece of code performs the following operations:
    1. Iterates through each datafiles and checks if new data
       was uploaded or not. There are situations when the webpage
       reject the requests made by the scrape, which leads to missin
       data if not tracked correctly.
    2. Sends notifications to slack
    '''

    with open('/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/{}'.format(file_name), 'rb') as inputfile:
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H')
        all_dates = []
        for item in json_lines.reader(inputfile):
            date_val = datetime.strptime(item['datetime'], '%Y-%m-%d %H:%M:%S')
            all_dates.append(date_val.strftime('%Y-%m-%d %H'))

        if now in all_dates:

            unicode = "\u2705"
            status = "Success"

        else:

            unicode = "\u274C"
            status = "Fail"

    # Send Slack notifications
    hf.slack_msg("""
    ```
    datafile: {},
    status: {}
    ```
    """.format(unicode+file_name, status))

def main():

    # data_check("company_profile.jl")
    data_check("index.jl")
    data_check("stock_prices.jl")

if __name__ == "__main__":
    main()
