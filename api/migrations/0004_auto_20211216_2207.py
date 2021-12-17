# Generated by Django 3.2.9 on 2021-12-16 13:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211202_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='meeting_url',
            field=models.CharField(blank=True, max_length=256, validators=[django.core.validators.RegexValidator(regex='^https://(meet.google.com|[A-Za-z0-9]+.zoom.us)/[A-Za-z0-9/?=-]+$')], verbose_name='ミーティングURL'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='プロフィール画像URL'),
        ),
    ]
