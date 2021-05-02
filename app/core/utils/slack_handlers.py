from slacker import Slacker
from app.core.config import load_config
from pandas.io.json import json_normalize
import requests

CONFIG = load_config()

class SlackHandler():
    def __int__(self):
        pass

    def send_message(self, text):
        token = CONFIG.SLACK_TOKEN
        response = requests.post("https://slack.com/api/chat.postMessage",
                                 headers={"Authorization": "Bearer " + token},
                                 data={"channel": "#server-log", "text": text}
                                 )
        print(response)
