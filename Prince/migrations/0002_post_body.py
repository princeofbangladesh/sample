# Generated by Django 2.2.6 on 2019-10-11 18:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Prince', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(default=datetime.datetime(2019, 10, 11, 18, 12, 3, 367234, tzinfo=utc), max_length=220),
            preserve_default=False,
        ),
    ]
