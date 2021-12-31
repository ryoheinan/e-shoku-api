from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models import Q
import urllib.parse
from .models import MyUser, Room
from .serializers import UserIdSerializer, UserSerializer, RoomSerializer, RoomFullSerializer


class UserAPIView(views.APIView):
    """
    ユーザモデルの取得(一覧)・登録APIクラス
    """

    def get(self, request, *args, **kwargs):
        """
        ユーザモデルの取得APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=request.user.pk)
        # シリアライザオブジェクトを作成
        serializer = UserSerializer(instance=user)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        ユーザモデルの登録APIに対応するハンドラメソッド
        """

        user_info = request.data.copy()
        user_info['internal_id'] = request.user.internal_id
        serializer = UserSerializer(instance=request.user, data=user_info)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyAPIView(views.APIView):
    """
    ユーザモデルの取得(詳細)・更新・一部更新・削除APIクラス
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        """ユーザモデルの取得(詳細)APIに対応するハンドラメソッド"""
        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk, is_info_filled=True)
        # シリアライザオブジェクトを作成
        serializer = UserSerializer(instance=user)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        ユーザモデルの更新APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
        if user != request.user:
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # シリアライザオブジェクトを作成
        serializer = UserSerializer(instance=user, data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """
        ユーザモデルの一部更新APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
        if user != request.user:
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # モデルオブジェクトを作成
        serializer = UserSerializer(
            instance=user, data=request.data, partial=True)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを一部更新
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        """
        ユーザモデルの削除APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
        if user != request.user:
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # モデルオブジェクトを削除
        user.delete()
        # レスポンスオブジェクトを返す
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomFilter(filters.FilterSet):
    """
    ルームモデルのフィルタクラス
    """

    datetime = filters.DateTimeFilter(lookup_expr='gte')

    class Meta:
        model = Room
        exclude = ['meeting_url']


class RoomAPIView(views.APIView):
    """
    ルームモデルの取得(一覧)・登録APIクラス
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        ルームモデルの取得(一覧)APIに対応するハンドラメソッド
        """

        # query_paramsにrelated_userが含まれている場合は、そのユーザーに関連するルームを取得する
        related_user = request.query_params.get('related_user')
        # query_paramsにqが含まれている場合は、その文字列に関連するルームを取得する
        keyword = request.query_params.get('q')
        if related_user:
            related_user = urllib.parse.unquote(related_user)
            # 非公開ルームが含まれるため認証済みユーザーのみルーム情報を取得する
            if related_user != str(request.user.id):
                raise exceptions.AuthenticationFailed('Unauthorized access')
            room_data = Room.objects.filter(Q(hosts=related_user) | Q(
                guests=related_user)).distinct().order_by('-datetime')
            filterset = RoomFilter(request.query_params, queryset=room_data)
        elif keyword:
            keyword = urllib.parse.unquote(keyword)
            # 大文字小文字区別なく、部分一致で検索する
            room_data = Room.objects.filter(Q(room_name__icontains=keyword) | Q(
                description__icontains=keyword), is_private=False).distinct().order_by('-datetime')
            filterset = RoomFilter(request.query_params, queryset=room_data)
        else:
            # モデルオブジェクトの一覧をフィルタリング
            filterset = RoomFilter(request.query_params,
                                   queryset=Room.objects.filter(is_private=False).order_by('datetime'))
        # シリアライザオブジェクトを作成
        serializer = RoomSerializer(instance=filterset.qs, many=True)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        ルームモデルの登録APIに対応するハンドラメソッド
        """

        # シリアライザオブジェクトを作成
        serializer = RoomFullSerializer(data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_201_CREATED)


class RoomRetrieveUpdateDestroyAPIView(views.APIView):
    """
    ルームモデルの取得(詳細)・更新・一部更新・削除APIクラス
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        """
        ルームモデルの取得(詳細)APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        # 主催者・参加者のみがmeeting_urlを参照できるようにする
        if request.user not in room.guests.all() and request.user not in room.hosts.all():
            serializer = RoomSerializer(instance=room)
        else:
            serializer = RoomFullSerializer(instance=room)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        ルームモデルの更新APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        if not room.hosts.filter(pk=request.user.id).exists():
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # シリアライザオブジェクトを作成
        serializer = RoomFullSerializer(instance=room, data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """
        ルームモデルの一部更新APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        if not room.hosts.filter(pk=request.user.id).exists():
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # モデルオブジェクトを作成
        serializer = RoomFullSerializer(
            instance=room, data=request.data, partial=True)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを一部更新
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        """
        ルームモデルの削除APIに対応するハンドラメソッド
        """

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        if not room.hosts.filter(pk=request.user.id).exists():
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # モデルオブジェクトを削除
        room.delete()
        # レスポンスオブジェクトを返す
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomJoinAPIView(views.APIView):
    """
    ルーム参加APIのためのクラス
    """

    def post(self, request, pk, *args, **kwargs):
        """
        ルーム参加APIに対応するハンドラメソッド
        """

        serializer = UserIdSerializer(data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['id']
        if user_id != request.user.id:
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        user = get_object_or_404(MyUser, pk=user_id)
        # ユーザーをルームに参加
        try:
            room.join(user)
        except ValueError as e:
            raise exceptions.ValidationError({"detail": e})
        # レスポンスオブジェクトを返す
        return Response({'status': 'successfully joined'}, status=status.HTTP_200_OK)


class RoomLeaveAPIView(views.APIView):
    """
    ルーム参加キャンセルAPIのためのクラス
    """

    def post(self, request, pk, *args, **kwargs):
        """
        ルーム参加キャンセルAPIに対応するハンドラメソッド
        """

        serializer = UserIdSerializer(data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['id']
        if user_id != request.user.id:
            raise exceptions.AuthenticationFailed('Unauthorized access')
        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        user = get_object_or_404(MyUser, pk=user_id)
        # ルームへの参加キャンセル
        try:
            room.leave(user)
        except ValueError as e:
            raise exceptions.ValidationError({"detail": e})
        # レスポンスオブジェクトを返す
        return Response({'status': 'successfully left'}, status=status.HTTP_200_OK)
