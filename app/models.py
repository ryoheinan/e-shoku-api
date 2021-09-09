from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, display_name, date_of_birth, gender, password=None):
        """
        ユーザー作成時のプログラム
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
            display_name=display_name,
            date_of_birth=date_of_birth,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, display_name, date_of_birth, gender, password=None):
        """
        superuser作成時のプログラム
        """
        user = self.create_user(
            email,
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
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='ユーザーネーム', max_length=20, unique=True)
    display_name = models.CharField(verbose_name='名前', max_length=100)
    date_of_birth = models.DateField(
        verbose_name='生年月日', null=True, blank=True)
    gender = models.CharField(verbose_name='性別', max_length=6, choices=[
        ('MALE', '男性'), ('FEMALE', '女性'), ('PNTS', '無回答'), ('OTHERS', 'その他')])
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'display_name', 'date_of_birth', 'gender']

    def __str__(self):
        return self.email

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ManyToManyField(MyUser, verbose_name='ユーザー')
    role = models.CharField(verbose_name='役職', max_length=5, choices=[
                            ('HOST', '主催者'), ('GUEST', '参加者')])
    room_name = models.CharField(verbose_name='ルーム名', max_length=20)
    members = models.IntegerField(verbose_name='人数', default=6)
    topic = models.TextField(verbose_name='トピック')
    invite_code = models.IntegerField(
        verbose_name='招待コード', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
