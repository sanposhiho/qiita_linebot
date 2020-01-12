from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import urllib.request
import json


REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
PUSH_ENDPOINT_URL = "https://api.line.me/v2/bot/message/push"

LINE_ACCESSTOKEN = settings.LINE_ACCESSTOKEN

HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_ACCESSTOKEN
}

class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token, user_id):
        body = {
            'replyToken': reply_token,
            'messages': self.messages
        }
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
            #print('pushメッセージを使用して再送します。')
            #body = {
            #    'to': user_id,
            #    'messages': self.messages
            #}
            #req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        except urllib.error.URLError as err:
            print(err.reason)

