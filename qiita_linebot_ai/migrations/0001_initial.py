# Generated by Django 3.0.1 on 2020-01-10 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('line_user_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('qiita_access_token', models.CharField(max_length=200)),
            ],
        ),
    ]
