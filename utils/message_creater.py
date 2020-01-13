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
    notification = {
              "type": "button",
              "style": "primary",
              'height': 'sm',
              'margin': 'xl',
              "action": {
                "type": "postback",
                "label": "通知",
                "displayText": "通知を確認する",
                "data": "notification"
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
    contents.append(notification)
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

def create_tag_new_items_message(tag):
    tag_items = qiita_tools.get_tag_new_items(tag)
    contents = []
    for i,tag_item in enumerate(tag_items):
        title = tag_item['title'].replace('\u3000', ' ')
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
                                "label": str(index) +"/5 (詳しく見る)",
                                "displayText": str(index)+"/5 を詳しく見る",
                                "data": "tag_item&"+tag+"&"+str(index-1)
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
                    "uri": tag_item['url']
                  }
                }
        contents.append(content)
    message = [{
                "type": "flex",
                "altText": tag +"の最新記事はこちらです！",
                "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": tag +"の最新記事はこちらです！",
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

def create_tag_new_items_message_index(tag, index):
    tag_items = qiita_tools.get_tag_new_items(tag)
    messages = []
    for i,tag_item in enumerate(tag_items):
        if index*5 <= i and i < index*5 + 5:
            title = tag_item['title'].replace('\u3000', ' ')
            url = tag_item['url']
            message = {
                        'type': 'text',
                        'text': title + '\n' + url
                    }
            messages.append(message)
    return messages

def create_auth_user_notifications_message(user):
    notification_with_item_info = qiita_tools.get_auth_user_notifications(user)
    messages = []
    for notification_info in notification_with_item_info:
        notification = notification_info['notifications']
        if notification['comments'] == [] and notification['likes'] == []:
            continue
        item = notification_info['item']
        contents = []
        if not notification['comments'] == []:
            comments = "過去1日に"+str(len(notification['comments']))+'件のコメントがつきました'
            comment_message = {
                              "type": "text",
                              "text": comments,
                              "size": "md",
                              "align": "start",
                            }
            contents.append(comment_message)

        if not notification['likes'] == []:
            likes = "過去1日に"+str(len(notification['likes']))+'件のいいねがつきました'
            like_message = {
                              "type": "text",
                              "text": likes,
                              "size": "md",
                              "align": "start",
                            }
            contents.append(like_message)

        message_contents = {
                  "type": "box",
                  "layout": "vertical",
                  "spacing": "md",
                  "contents":contents
                }
        message = {
                  "type": "box",
                  "layout": "vertical",
                  "spacing": "md",
                  "margin": "xl",
                  "contents":[
                    {
                        "type": "separator"
                    },
                    {
                      "type": "button",
                      "style": "link",
                      'height': 'sm',
                      'margin': 'xs',
                      "action": {
                        "type": "uri",
                        "label": item['title'],
                        "uri": item['url']
                      }
                    },
                    message_contents
                  ]
                }
        messages.append(message)
    return_messages = []
    if messages == []:
        return_messages = create_single_text_message("新着の通知はありません！")
    else:
        for message in messages:
            message = [message]
            return_message = {
                        "type": "flex",
                        "altText": "Qiitaの通知です！",
                        "contents": {
                        "type": "bubble",
                        "body": {
                          "type": "box",
                          "layout": "vertical",
                          "spacing": "md",
                          "contents": message
                        }
                        }
                    }
            return_messages.append(return_message)
    return return_messages
