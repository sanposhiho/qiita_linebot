from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import urllib.request
import json
import ast

from utils import message_creater
from qiita_linebot_ai.line_message import LineMessage

QIITA_OAUTH_URL = 'https://qiita.com/api/v2/oauth/authorize'
QIITA_ACCESSTOKEN_URL = 'https://qiita.com/api/v2/access_tokens'

QIITA_CLIENT_ID = settings.QIITA_CLIENT_ID
QIITA_CLIENT_SECRET = settings.QIITA_CLIENT_SECRET

LINE_GROUP_URL = settings.LINE_GROUP_URL

NGROK_HOST = settings.NGROK_HOST

@csrf_exempt
def index(request):
    if request.method == 'POST':
        line_request = json.loads(request.body.decode('utf-8'))
        events = line_request['events']
        for event in events:
            message = event['message']
            reply_token = event['replyToken']
            if message['text'] == 'login':
                if 'qiita_access_token' not in request.session:
                    oauth_message = '以下のURLからQiitaで認証を行なってください\n' + QIITA_OAUTH_URL + '?client_id=' + QIITA_CLIENT_ID + '&scope=read_qiita+write_qiita'
                    line_message = LineMessage(message_creater.create_single_text_message(oauth_message))
                    line_message.reply(reply_token)
                else:
                    message = 'すでにログイン済みです'
                    line_message = LineMessage(message_creater.create_single_text_message(message))
                    line_message.reply(reply_token)
        return HttpResponse("ok")

@csrf_exempt
def oauth(request):
    if request.method == 'GET':
        if "code" in request.GET:
            code = request.GET.get("code")
            body = {
                    'client_id': QIITA_CLIENT_ID,
                    'client_secret': QIITA_CLIENT_SECRET,
                    'code': code
                    }
            header = {
                    'Content-Type': 'application/json',
                    }
            req = urllib.request.Request(QIITA_ACCESSTOKEN_URL, json.dumps(body).encode(), header)
            try:
                with urllib.request.urlopen(req) as res:
                    body = res.read().decode("utf-8")
                    request.session['qiita_access_token'] = ast.literal_eval(body)['token']
                    return redirect('https://lin.ee/vJgES3p')
            except urllib.error.HTTPError as err:
                print(err)
                return redirect('https://lin.ee/vJgES3p')
            except urllib.error.URLError as err:
                print(err.reason)
                return redirect('https://lin.ee/vJgES3p')

        else:
            return redirect('https://lin.ee/vJgES3p')
