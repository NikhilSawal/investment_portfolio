import requests
import json
import os

def slack_msg(msg):

    """This method is called from different scripts (all spiders currently) to send
    notification to slack about the completion of jobs. This script also sources the
    SLACK_API_KEY, which is a global environment variable, that can be sourced from
    the ./bashprofile in root directory and contab files."""

    data = {
        "text" : msg
    }

    webhook = os.environ.get("SLACK_API_KEY")
    requests.post(webhook, json.dumps(data))


def get_working_ip(proxy):

    """This method is not currently in operation, but will soon be put to use the
    frequency of scrape needs to be increased to gather information on shorter time
    spans. This method will try a set of ip's for the spider to scrape the given weblink
    and would return ip's that work with the website, to avoid the system ip from getting
    blocked."""

    try:
        r = requests.get('https://finance.yahoo.com/', proxies={'http':proxy, 'https':proxy}, timeout=randrange(7, 15))
        print(r.json(), ' - working')
    except:
        print('Not working')
    return proxy
