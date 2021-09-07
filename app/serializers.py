from rest_framework import serializers

from .models import User, Room


class UserSerializer(serializers.ModelSerializer):
    """ユーザモデル用シリアライザ"""

    class Meta:
        # 対象モデルクラスを指定
        model = User
        # 利用しないモデルのフィールドを指定
        exclude = ['created_at']


class UserListSerializer(serializers.ListSerializer):
    """複数モデルを扱うためのシリアライザ"""
    child = UserSerializer()


class RoomSerializer(serializers.ModelSerializer):
    """ルームモデル用シリアライザ"""

    class Meta:
        # 対象モデルクラスを指定
        model = Room
        # 利用しないモデルのフィールドを指定
        exclude = ['created_at']


class RoomListSerializer(serializers.ListSerializer):
    """複数モデルを扱うためのシリアライザ"""
    child = RoomSerializer()
