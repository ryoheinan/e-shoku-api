# Generated by Django 3.2.6 on 2021-10-07 13:07

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=128, unique=True, verbose_name='auth0識別子')),
                ('username', models.CharField(max_length=128, unique=True, verbose_name='ユーザーネーム')),
                ('display_name', models.CharField(max_length=100, verbose_name='名前')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='生年月日')),
                ('gender', models.CharField(choices=[('MALE', '男性'), ('FEMALE', '女性'), ('PNTS', '無回答'), ('OTHERS', 'その他')], max_length=6, verbose_name='性別')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('HOST', '主催者'), ('GUEST', '参加者')], max_length=5, verbose_name='役職')),
                ('room_name', models.CharField(max_length=20, verbose_name='ルーム名')),
                ('members', models.IntegerField(default=6, verbose_name='人数')),
                ('topic', models.TextField(verbose_name='トピック')),
                ('invite_code', models.IntegerField(blank=True, null=True, verbose_name='招待コード')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'db_table': 'room',
            },
        ),
    ]
