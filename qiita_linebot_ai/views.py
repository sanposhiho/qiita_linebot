from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from qiita_linebot_ai.models import User
import urllib.request
import json
import ast
import random

from utils import message_creater, qiita_tools
from qiita_linebot_ai.line_message import LineMessage

QIITA_OAUTH_URL = 'https://qiita.com/api/v2/oauth/authorize'
QIITA_ACCESSTOKEN_URL = 'https://qiita.com/api/v2/access_tokens'

QIITA_CLIENT_ID = settings.QIITA_CLIENT_ID
QIITA_CLIENT_SECRET = settings.QIITA_CLIENT_SECRET

LINE_OAUTH_URL = 'https://access.line.me/dialog/oauth/weblogin'
LINE_ACCESSTOKEN_URL = 'https://api.line.me/v2/oauth/accessToken'
LINE_GROUP_URL = settings.LINE_GROUP_URL
LINE_CHANNEL_ID = settings.LINE_CHANNEL_ID
LINE_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET

LINE_REDIRECT_URL = 'https://ecdb2a20.ngrok.io/qiita_linebot_ai/oauth/line/'

@csrf_exempt
def index(request):
    if request.method == 'POST':
        line_request = json.loads(request.body.decode('utf-8'))
        events = line_request['events']
        for event in events:
            reply_token = event['replyToken']
            user_id = event['source']['userId']
            #Postback
            if 'postback' in event:
                postback_data = event['postback']['data'].split('&')
                target = postback_data[0]

                #トレンド詳細
                if target == "trend":
                    data = postback_data[1]
                    message = message_creater.create_qiita_trend_items_message_index(index=int(data))
                    line_message = LineMessage(message)
                    line_message.reply(reply_token)

                #トレンド
                elif target == 'alltrend':
                    message = message_creater.create_qiita_trend_items_message()
                    line_message = LineMessage(message)
                    line_message.reply(reply_token)

                #タグ
                elif target == 'allfollow_tag':
                    try:
                        user = User.objects.get(pk=user_id)
                        message = message_creater.create_tag_index_message(user)
                        line_message = LineMessage(message)
                        line_message.reply(reply_token)
                    except User.DoesNotExist:
                        oauth_message = '以下のURLからQiita認証を行ってください！\n' + 'https://ecdb2a20.ngrok.io' + reverse("qiita_linebot_ai:login", args=[user_id])
                        line_message = LineMessage(message_creater.create_single_text_message(oauth_message))
                        line_message.reply(reply_token)

                #タグトレンド
                elif target == 'follow_tag_trend':
                    tag = postback_data[1]
                    message = message_creater.create_qiita_tag_trend_items_message(tag)
                    line_message = LineMessage(message)
                    line_message.reply(reply_token)

                #タグ最新記事
                elif target == 'follow_tag_index':
                    tag = postback_data[1]
                    message = message_creater.create_tag_new_items_message(tag)
                    line_message = LineMessage(message)
                    line_message.reply(reply_token)

                #ログイン
                elif target == 'login':
                    try:
                        user = User.objects.get(pk=user_id)
                        message = 'すでにログイン済みです！'
                        line_message = LineMessage(message_creater.create_single_text_message(message))
                        line_message.reply(reply_token)
                    except User.DoesNotExist:
                        oauth_message = '以下のURLからQiita認証を行ってください！\n' + 'https://ecdb2a20.ngrok.io' + reverse("qiita_linebot_ai:login", args=[user_id])
                        line_message = LineMessage(message_creater.create_single_text_message(oauth_message))
                        line_message.reply(reply_token)

            else:
                message = message_creater.create_index_message()
                line_message = LineMessage(message)
                line_message.reply(reply_token)

        return HttpResponse("ok")

def login(request, user_id):
    if request.method == 'GET':
        state = random.randint(1,100000)
        request.session['qiita_state'] = state
        request.session['line_user_id'] = user_id
        return redirect(QIITA_OAUTH_URL + '?client_id=' + QIITA_CLIENT_ID + '&state=' + str(state) + '&scope=read_qiita+write_qiita')

@csrf_exempt
def qiita_oauth(request):
    if request.method == 'GET':
        state = request.session['qiita_state']
        if state == int(request.GET.get("state")):
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
                        user = User(qiita_access_token=ast.literal_eval(body)['token'], line_user_id=request.session['line_user_id'])
                        user.save()
                        #state = random.randint(1,100000)
                        #request.session['line_state'] = state
                        #line_oauth_url = LINE_OAUTH_URL + '?response_type=code&client_id=' + LINE_CHANNEL_ID + '&redirect_uri=' + LINE_REDIRECT_URL + '&state=' + str(state)
                        #return redirect(line_oauth_url)
                        return redirect(LINE_GROUP_URL)
                except urllib.error.HTTPError as err:
                    print(err)
                    return redirect(LINE_GROUP_URL)
                except urllib.error.URLError as err:
                    print(err.reason)
                    return redirect(LINE_GROUP_URL)

            else:
                return redirect(LINE_GROUP_URL)
    return HttpResponse("ok")

@csrf_exempt
def line_oauth(request):
    if request.method == 'GET':
        state = request.session['line_state']
        if state == int(request.GET.get("state")):
            print("ok")
            code = request.GET.get("code")
            body = {
                    'grant_type': 'authorization_code',
                    'client_id': LINE_CHANNEL_ID,
                    'client_secret': LINE_CHANNEL_SECRET,
                    'code': code,
                    'redirect_uri': LINE_REDIRECT_URL
                    }
            header = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    }
            req = urllib.request.Request(LINE_ACCESSTOKEN_URL, json.dumps(body).encode(), header)
            try:
                with urllib.request.urlopen(req) as res:
                    body = res.read().decode("utf-8")
                    request.session['line_access_token'] = ast.literal_eval(body)['token']
                    return redirect(LINE_GROUP_URL)
            except urllib.error.HTTPError as err:
                print(err)
                return redirect(LINE_GROUP_URL)
            except urllib.error.URLError as err:
                print(err.reason)
                return redirect(LINE_GROUP_URL)
    return HttpResponse("ok")
