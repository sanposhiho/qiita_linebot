from django.db import models

LINE_VALIFY_ACCESS_TOKEN_URL = 'https://api.line.me/v2/oauth/verify'

class User(models.Model):
    line_user_id = models.CharField(max_length=200, primary_key=True)
    qiita_access_token = models.CharField(max_length=200)
    #line_access_token = models.CharField(max_length=200)
