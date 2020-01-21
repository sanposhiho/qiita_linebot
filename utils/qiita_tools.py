import datetime
import urllib.request
from bs4 import BeautifulSoup
import json
from django.utils import timezone

QIITA_TOP_URL = 'https://qiita.com/'

def get_trend_items(scope):
    if scope == "daily":
        req = urllib.request.Request(QIITA_TOP_URL)
    elif scope == "monthly":
        req = urllib.request.Request(QIITA_TOP_URL+"?scope=monthly")
    elif scope == "weekly":
        req = urllib.request.Request(QIITA_TOP_URL+"?scope=weekly")
    with urllib.request.urlopen(req) as res:
        body = res.read()
    soup = BeautifulSoup(body, "html.parser")
    target_div = soup.select('div[data-hyperapp-app="Trend"]')[0]
    trend_items = json.loads(target_div.get('data-hyperapp-props'))
    return trend_items

def get_items_uri(user_id, uuid):
    return QIITA_TOP_URL + user_id + '/items/' + uuid

def get_tag_trend_items(tag):
    req = urllib.request.Request(QIITA_TOP_URL+'tags/'+tag)
    with urllib.request.urlopen(req) as res:
        body = res.read()
    soup = BeautifulSoup(body, "html.parser")
    trend_items = []
    for target in soup.select('article[data-test-tag-trend-article-uuid]'):
        target = target.select('div[class="tst-ArticleBody"]')[0].select('a[class="tst-ArticleBody_title"]')[0]
        target_url = target['href']
        target_title = target.string
        target = {
                'url':QIITA_TOP_URL + target_url,
                'title':target_title
                }
        trend_items.append(target)
    return trend_items

def get_qiita_user_info(user):
    access_token = user.qiita_access_token
    header = {
            'Authorization': 'Bearer '+access_token,
            'content-type'  : 'application/json',
            }
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/authenticated_user', headers = header)
    with urllib.request.urlopen(req) as res:
        body = res.read()
    user_info = json.loads(body)
    return user_info

def get_following_tags(user):
    user_info = get_qiita_user_info(user)
    user_id = user_info['id']
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/users/'+user_id+'/following_tags?page=1&per_page=15')
    with urllib.request.urlopen(req) as res:
        body = res.read()
    following_tags = json.loads(body)
    return following_tags

def get_tag_new_items(tag):
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/tags/'+tag+'/items?page=1&per_page=25')
    with urllib.request.urlopen(req) as res:
        body = res.read()
    items = json.loads(body)
    return items

def get_auth_user_notifications(user):
    items = get_auth_user_items(user)
    notifications = []
    for item in items:
        item_id = item['id']
        notification = check_item_notifications(item_id)
        notification_with_item_info = {
                'notifications': notification,
                'item': item
                }
        notifications.append(notification_with_item_info)
    return notifications

def get_auth_user_items(user):
    access_token = user.qiita_access_token
    header = {
            'Authorization': 'Bearer '+access_token,
            'content-type'  : 'application/json',
            }
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/authenticated_user/items?page=1&per_page=5', headers=header)
    with urllib.request.urlopen(req) as res:
        body = res.read()
    items = json.loads(body)
    return items

def check_item_notifications(item_id):
    comments = get_item_comments(item_id)
    comments = list(filter(lambda x: datetime.datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%S%z') >= timezone.now() - datetime.timedelta(days=1), comments))
    likes = get_item_likes(item_id)
    likes = list(filter(lambda x: datetime.datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%S%z') >= timezone.now() - datetime.timedelta(days=1), likes))
    notifications = {
                    'comments': comments,
                    'likes': likes
                    }
    return notifications

def get_item_comments(item_id):
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/items/'+item_id+'/comments')
    with urllib.request.urlopen(req) as res:
        body = res.read()
    comments = json.loads(body)
    return comments

def get_item_likes(item_id):
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/items/'+item_id+'/likes')
    with urllib.request.urlopen(req) as res:
        body = res.read()
    likes = json.loads(body)
    return likes
