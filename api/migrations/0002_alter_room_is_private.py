# Generated by Django 3.2.8 on 2021-11-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='非公開'),
        ),
    ]
