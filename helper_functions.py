import requests
import json
import os

def slack_msg(msg):

    data = {
        "text" : msg
    }

    webhook = os.environ.get("SLACK_API_KEY")
    requests.post(webhook, json.dumps(data))
