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
