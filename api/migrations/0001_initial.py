# Generated by Django 3.2.8 on 2021-11-20 11:21

from django.conf import settings
import django.core.validators
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
                ('username', models.CharField(default=uuid.uuid4, max_length=128, unique=True, verbose_name='ユーザーネーム')),
                ('display_name', models.CharField(max_length=100, verbose_name='名前')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='生年月日')),
                ('gender', models.CharField(choices=[('MALE', '男性'), ('FEMALE', '女性'), ('PNTS', '無回答'), ('OTHERS', 'その他')], max_length=6, verbose_name='性別')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('is_info_filled', models.BooleanField(default=False)),
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
                ('room_name', models.CharField(max_length=128, verbose_name='ルーム名')),
                ('description', models.TextField(verbose_name='ルームの説明')),
                ('datetime', models.DateTimeField(blank=True, null=True, verbose_name='開催日時')),
                ('capacity', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='定員')),
                ('topic', models.TextField(blank=True, null=True, verbose_name='トピック')),
                ('invite_code', models.IntegerField(blank=True, null=True, unique=True, verbose_name='招待コード')),
                ('is_private', models.BooleanField(verbose_name='非公開')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('guests', models.ManyToManyField(blank=True, related_name='guest_users', to=settings.AUTH_USER_MODEL, verbose_name='参加者')),
                ('hosts', models.ManyToManyField(related_name='host_users', to=settings.AUTH_USER_MODEL, verbose_name='主催者')),
            ],
            options={
                'db_table': 'room',
            },
        ),
    ]
