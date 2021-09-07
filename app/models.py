import uuid
from django.db import models


class User(models.Model):
    """ユーザーモデル"""
    class Meta:
        db_table = 'user'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='名前', max_length=20, unique=True)
    address = models.CharField(
        verbose_name='メールアドレス', max_length=30, unique=True)
    age = models.IntegerField(verbose_name='年齢', null=True, blank=True)
    sex = models.CharField(verbose_name='性別', choices=('男性', '女性'))
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


class Room(models.Model):
    """ルームモデル"""
    class Meta:
        db_table = 'room'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(User, verbose_name='ユーザー')
    role = models.CharField(verbose_name='役職', choices=('主催者', '参加者'))
    room_name = models.CharField(verbose_name='ルーム名', max_length=20)
    members = models.IntegerField(verbose_name='人数', default=6, max_length=2)
    topic = models.TextField(verbose_name='トピック')
    invite_code = models.IntegerField(
        verbose_name='招待コード', max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
