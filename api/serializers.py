from rest_framework import serializers
from .models import MyUser, Room


class UserSerializer(serializers.ModelSerializer):
    """
    ユーザモデル用シリアライザ
    """

    class Meta:
        # 対象モデルクラスを指定
        model = MyUser
        # 利用しないモデルのフィールドを指定
        exclude = ['password', 'created_at',
                   'last_login', 'is_active', 'is_admin']

    def update(self, instance, validated_data):
        """
        ModelSerializerのupdate関数をオーバーライドした関数
        """

        super().update(instance, validated_data)
        instance.is_info_filled = True
        instance.save()
        return instance


class UserListSerializer(serializers.ListSerializer):
    """
    複数モデルを扱うためのシリアライザ
    """

    child = UserSerializer()


class RoomSerializer(serializers.ModelSerializer):
    """
    ルームモデル用シリアライザ
    """

    class Meta:
        # 対象モデルクラスを指定
        model = Room
        # 利用しないモデルのフィールドを指定
        exclude = ['created_at']


class RoomListSerializer(serializers.ListSerializer):
    """
    複数モデルを扱うためのシリアライザ
    """

    child = RoomSerializer()
