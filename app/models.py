import uuid
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUser(models.Model):
    """ユーザーモデル"""
    class Meta:
        db_table = 'custom_user'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name='ユーザーネーム', max_length=20, unique=True)
    display_name = models.CharField(verbose_name='名前', max_length=100)
    password = models.CharField(
        verbose_name='パスワード', max_length=128)
    email = models.EmailField(
        verbose_name='メールアドレス', max_length=256, unique=True)
    age = models.IntegerField(verbose_name='年齢', null=True, blank=True)
    gender = models.CharField(verbose_name='性別', max_length=6, choices=[
        ('MALE', '男性'), ('FEMALE', '女性'), ('PNTS', '無回答'), ('OTHERS', 'その他')])
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)


class Room(models.Model):
    """ルームモデル"""
    class Meta:
        db_table = 'room'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(CustomUser, verbose_name='ユーザー')
    role = models.CharField(verbose_name='役職', max_length=5, choices=[
                            ('HOST', '主催者'), ('GUEST', '参加者')])
    room_name = models.CharField(verbose_name='ルーム名', max_length=20)
    members = models.IntegerField(verbose_name='人数', default=6)
    topic = models.TextField(verbose_name='トピック')
    invite_code = models.IntegerField(
        verbose_name='招待コード', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
