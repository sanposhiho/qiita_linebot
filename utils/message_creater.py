from utils import message_creater, qiita_tools

def create_single_text_message(message):
    text_message = [
                {
                    'type': 'text',
                    'text': message
                }
            ]
    return text_message

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
