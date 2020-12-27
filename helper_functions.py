import requests
import json
import os

def slack_msg(msg):

    data = {
        "text" : msg
    }

    webhook = os.environ.get("SLACK_API_KEY")
    requests.post(webhook, json.dumps(data))


def get_working_ip(proxy):

    try:
        r = requests.get('https://finance.yahoo.com/', proxies={'http':proxy, 'https':proxy}, timeout=randrange(7, 15))
        print(r.json(), ' - working')
    except:
        print('Not working')
    return proxy

# get_working_ip('177.69.23.177:80')

# with open('/Users/nikhilsawal/OneDrive/investment_portfolio/ip.json') as f:
#     df = json.load(f)
#
# for index in range(len(df)):
#     print(index, get_working_ip(str(df[index]['ip_address']) + ':' + str(df[index]['port'])))
