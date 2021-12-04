from rest_framework import serializers
from .models import MyUser, Room
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    """
    ユーザモデル用シリアライザ
    """

    class Meta:
        # 対象モデルクラスを指定
        model = MyUser
        # 利用しないモデルのフィールドを指定
        exclude = ['password', 'last_login', 'is_active', 'is_admin']
        # 読み込み専用フィールドを指定
        read_only_fields = ['created_at']

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


class UserMinInfoSerializer(serializers.ModelSerializer):
    """
    最小限のユーザ情報を提供するシリアライザ
    """

    class Meta:
        # 対象モデルクラスを指定
        model = MyUser
        # 利用するモデルのフィールドを指定
        fields = ['id', 'username']


class UserIdSerializer(serializers.Serializer):
    """
    ユーザIDのみを扱うシリアライザ
    """

    id = serializers.UUIDField(format='hex_verbose')


class RoomSerializer(serializers.ModelSerializer):
    """
    ルームモデル用シリアライザ
    """

    class Meta:
        # 対象モデルクラスを指定
        model = Room
        # 読み込み専用フィールドを指定
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not settings.IS_TEST:
            ret['hosts'] = UserMinInfoSerializer(
                instance.hosts.all(), many=True).data
            ret['guests'] = UserMinInfoSerializer(
                instance.guests.all(), many=True).data
            ret['hosts_count'] = instance.hosts.all().count()
            ret['guests_count'] = instance.guests.all().count()
        return ret


class RoomListSerializer(serializers.ListSerializer):
    """
    複数モデルを扱うためのシリアライザ
    """

    child = RoomSerializer()
