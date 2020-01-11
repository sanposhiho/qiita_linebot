from utils import message_creater, qiita_tools

def create_single_text_message(message):
    text_message = [
                {
                    'type': 'text',
                    'text': message
                }
            ]
    return text_message

def create_index_message():
    login = {
              "type": "button",
              "style": "primary",
              'height': 'sm',
              'margin': 'xl',
              "action": {
                "type": "postback",
                "label": "Qiita紐付け",
                "displayText": "Qiitaと紐付ける",
                "data": "login"
              }
            }
    trend = {
              "type": "button",
              "style": "primary",
              'height': 'sm',
              'margin': 'xl',
              "action": {
                "type": "postback",
                "label": "トレンド",
                "displayText": "現在のトレンドを見る",
                "data": "alltrend"
              }
            }
    follow_tag = {
              "type": "button",
              "style": "primary",
              'height': 'sm',
              'margin': 'xl',
              "action": {
                "type": "postback",
                "label": "フォロー中タグ",
                "displayText": "フォロー中のタグを確認する",
                "data": "allfollow_tag"
              }
            }
    contents = []
    contents.append(login)
    contents.append(trend)
    contents.append(follow_tag)
    index_message = [{
                "type": "flex",
                "altText": "選択してくださいっ！",
                "contents": {
                "type": "bubble",
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "spacing": "md",
                  "contents": contents
                }
                }
            }]
    return index_message

def create_qiita_trend_items_message():
    trend_items = qiita_tools.get_trend_items()
    contents = []
    for i,trend_item in enumerate(trend_items['trend']['edges']):
        if i > 24:
            break
        title = trend_item['node']['title'].replace('\u3000', ' ')
        title_truncated = title[:37] + "..."
        if (i % 5) == 0:
            index = i // 5 + 1
            title_content = {
                              "type": "button",
                              "style": "link",
                              'height': 'sm',
                              'margin': 'xxl',
                              "action": {
                                "type": "postback",
                                "label": "トレンド "+ str(index) +"/5 (詳しく見る)",
                                "displayText": "トレンド "+str(index)+"/5 を詳しく見る",
                                "data": "trend&"+str(index-1)
                              }
                            }
            contents.append(title_content)
        content = {
                  "type": "button",
                  "style": "secondary",
                  'height': 'sm',
                  'margin': 'xs',
                  "action": {
                    "type": "uri",
                    "label": title_truncated,
                    "uri": qiita_tools.get_items_uri(trend_item['node']['author']['urlName'], trend_item['node']['uuid'])
                  }
                }
        contents.append(content)
    message = [{
                "type": "flex",
                "altText": "Qiitaの現在のトレンドの記事はこちらです！",
                "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "現在のQiitaのトレンドです！"
                      }
                    ]
                  },
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "spacing": "md",
                  "contents": contents
                }
                }
            }]
    return message

def create_qiita_trend_items_message_index(index):
    trend_items = qiita_tools.get_trend_items()
    messages = []
    for i,trend_item in enumerate(trend_items['trend']['edges']):
        if index*5 <= i and i < index*5 + 5:
            title = trend_item['node']['title'].replace('\u3000', ' ')
            url = qiita_tools.get_items_uri(trend_item['node']['author']['urlName'], trend_item['node']['uuid'])
            message = {
                        'type': 'text',
                        'text': title + '\n' + url
                    }
            messages.append(message)
    return messages

def create_qiita_tag_trend_items_message(tag):
    trend_items = qiita_tools.get_tag_trend_items(tag)
    messages = []
    for trend_item in trend_items:
        title = trend_item['title'].replace('\u3000', ' ')
        url = trend_item['url']
        message = {
                    'type': 'text',
                    'text': title + '\n' + url
                }
        messages.append(message)
    return messages

def create_tag_index_message(user):
    following_tags = qiita_tools.get_following_tags(user)
    contents = []
    for tag in following_tags:
        tag_id = tag['id']
        button_content = {
                  "type": "box",
                  "layout": "horizontal",
                  "spacing": "md",
                  "contents":[
                    {
                      "type": "button",
                      "style": "secondary",
                      'height': 'sm',
                      'margin': 'xs',
                      "action": {
                        "type": "postback",
                        "label": "最新記事一覧",
                        "displayText": tag_id+'の最新記事を確認',
                        "data": 'follow_tag_index&'+tag_id,
                      }
                    },
                    {
                      "type": "button",
                      "style": "secondary",
                      'height': 'sm',
                      'margin': 'xs',
                      "action": {
                        "type": "postback",
                        "label": "トレンド",
                        "displayText": tag_id+'のトレンドを確認',
                        'data': 'follow_tag_trend&'+tag_id,
                      }
                    }
                  ]
                }
        content = {
                  "type": "box",
                  "layout": "vertical",
                  "spacing": "md",
                  "margin": "xl",
                  "contents":[
                    {
                        "type": "separator"
                    },
                    {
                      "type": "text",
                      "text": tag_id,
                      "size": "md",
                      "align": "start",
                    },
                    button_content
                  ]
                }
        contents.append(content)
    message = [{
                "type": "flex",
                "altText": "follow中のタグ一覧です！",
                "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "follow中のタグ一覧です！"
                      }
                    ]
                  },
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "spacing": "md",
                  "contents": contents
                }
                }
            }]
    return message
