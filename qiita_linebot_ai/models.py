from django.db import models

LINE_VALIFY_ACCESS_TOKEN_URL = 'https://api.line.me/v2/oauth/verify'

class User(models.Model):
    line_user_id = models.IntegerField(primary_key=True)
    qiita_access_token = models.CharField(max_length=200)
    line_access_token = models.CharField(max_length=200)

    def valify_line_access_token(self):
        if self.line_access_token is None:
            return False
        else:
            
