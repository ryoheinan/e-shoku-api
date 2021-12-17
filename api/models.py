from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, internal_id, username, display_name, date_of_birth, gender, password=None):
        """
        ユーザー作成時のプログラム
        """
        if not internal_id:
            raise ValueError('Users must have an internal_id address')

        user = self.model(
            internal_id=internal_id,
            password=password,
            username=username,
            display_name=display_name,
            date_of_birth=date_of_birth,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, internal_id, username, display_name, date_of_birth, gender, password=None):
        """
        superuser作成時のプログラム
        """
        user = self.create_user(
            internal_id,
            password=password,
            username=username,
            display_name=display_name,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
    ユーザーモデル
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    internal_id = models.CharField(
        verbose_name='auth0識別子', max_length=128, unique=True)
    username = models.CharField(
        verbose_name='ユーザーネーム', max_length=128, default=uuid.uuid4, unique=True)
    display_name = models.CharField(verbose_name='名前', max_length=100)
    date_of_birth = models.DateField(
        verbose_name='生年月日', null=True, blank=True)
    gender = models.CharField(verbose_name='性別', max_length=6, choices=[
        ('MALE', '男性'), ('FEMALE', '女性'), ('PNTS', '無回答'), ('OTHERS', 'その他')])
    description = models.CharField(
        verbose_name='自己紹介', max_length=500, null=True, blank=True)
    image_url = models.URLField(
        verbose_name='プロフィール画像URL', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    is_info_filled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'internal_id'
    REQUIRED_FIELDS = ['username', 'display_name', 'date_of_birth', 'gender']

    def __str__(self):
        return self.internal_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Room(models.Model):
    """
    ルームモデル
    """

    class Meta:
        db_table = 'room'

    meeting_url_regex = RegexValidator(
        regex=r'^https://(meet.google.com|[A-Za-z0-9]+.zoom.us)/[A-Za-z0-9/?=-]+$')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hosts = models.ManyToManyField(
        MyUser, verbose_name='主催者', related_name='host_users')
    guests = models.ManyToManyField(
        MyUser, verbose_name='参加者', blank=True, related_name='guest_users')
    room_name = models.CharField(verbose_name='ルーム名', max_length=128)
    description = models.TextField(verbose_name='ルームの説明')
    datetime = models.DateTimeField(verbose_name='開催日時', null=True, blank=True)
    capacity = models.IntegerField(
        verbose_name='定員', validators=[MinValueValidator(1)], default=10)
    meeting_url = models.CharField(
        verbose_name='ミーティングURL', validators=[meeting_url_regex], max_length=256, blank=True)
    topic = models.TextField(verbose_name='トピック', null=True, blank=True)
    invite_code = models.IntegerField(
        verbose_name='招待コード', unique=True, null=True, blank=True)
    is_private = models.BooleanField(verbose_name='非公開', default=False)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)

    def __str__(self):
        return self.room_name

    def join(self, user):
        """
        ルームに参加する
        """
        if user not in self.guests.all():
            self.guests.add(user)
        else:
            raise ValueError('Invalid value')

    def leave(self, user):
        """
        ルームの参加をキャンセルする
        """
        if user in self.guests.all():
            self.guests.remove(user)
        else:
            raise ValueError('Invalid value')
