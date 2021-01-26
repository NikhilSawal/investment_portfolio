import json_lines
import json
import re

####################################################################################################
# Script to modify stock_prices.jl and save, cleaned and transformed version
delta_pattern = re.compile(r'(.?\d+\.\d+)(\s).?(.?\d+\.\d+).+')

with open('/Users/nikhilsawal/OneDrive/investment_portfolio/tst_file.jl','w') as outputfile:
    with open('/Users/nikhilsawal/OneDrive/investment_portfolio/stock_prices.jl', 'rb') as inputfile:
        for index, item in enumerate(json_lines.reader(inputfile)):
            if index < 1694:
                item['price'] = item['price'].replace(",","")
                item['delta'] = delta_pattern.sub(r'\1\2\3', item['delta']).split(" ")
                json.dump(item, outputfile)
                outputfile.write('\n')
            else:
                json.dump(item, outputfile)
                outputfile.write('\n')

# Following script performs data cleaning operations on index.jl
delta_perc_pattern = re.compile(r'(.?\d+\.\d+).+')

with open('/Users/nikhilsawal/OneDrive/investment_portfolio/tst_file.jl','w') as outputfile:
    with open('/Users/nikhilsawal/OneDrive/investment_portfolio/index.jl', 'rb') as inputfile:
        for index, item in enumerate(json_lines.reader(inputfile)):
            if index < 2:
                pass
            elif index > 1 & index < 97:
                item['s&p_500'] = item['s&p_500'].replace(",","")
                item['s&p_500_delta(%)'] = delta_perc_pattern.sub(r'\1', item['s&p_500_delta(%)'])
                item['dow_30'] = item['dow_30'].replace(",","")
                item['dow_30_delta(%)'] = delta_perc_pattern.sub(r'\1', item['dow_30_delta(%)'])
                item['nasdaq'] = item['nasdaq'].replace(",","")
                item['nasdaq_delta(%)'] = delta_perc_pattern.sub(r'\1', item['nasdaq_delta(%)'])
                json.dump(item, outputfile)
                outputfile.write('\n')
            else:
                json.dump(item, outputfile)
                outputfile.write('\n')

# Cleaned company_profile.jl
with open('/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/company_profile_1.jl','w') as outputfile:
    with open('/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/company_profile.jl', 'rb') as inputfile:
        for index, item in enumerate(json_lines.reader(inputfile)):
            # print(str(item['employee_count']).replace(",",""))
            item['employee_count'] = str(item['employee_count']).replace(",","")
            json.dump(item, outputfile)
            outputfile.write('\n')

####################################################################################################

# 01/26/2021
# Modifies stock_prices.jl data structure
# Separates delta to (delta_price, delta_price_perc)
import ast
import sys
import json

with open("/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/stock_prices_1.jl", "w") as outFile:
    with open("/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/stock_prices.jl") as inpFile:
        for i, j in enumerate(inpFile):
            j = ast.literal_eval(j)
            j['delta_price'] = j['delta'][0]
            j['delta_price_perc'] = j['delta'][1]
            del j['delta']
            desired_order = ['datetime', 'name', 'price', 'delta_price', 'delta_price_perc', 'top_3_news', 'news_source']
            reordered = {k: j[k] for k in desired_order}
            json.dump(reordered, outFile)
            outFile.write('\n')