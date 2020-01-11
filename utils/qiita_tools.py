import urllib.request
from bs4 import BeautifulSoup
import json

QIITA_TOP_URL = 'https://qiita.com/'

def get_trend_items():
    req = urllib.request.Request(QIITA_TOP_URL)
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
    req = urllib.request.Request(QIITA_TOP_URL+'/api/v2/users/'+user_id+'/following_tags?page=1&per_page=100')
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
