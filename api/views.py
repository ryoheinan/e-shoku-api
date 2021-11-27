from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import MyUser, Room
from .serializers import UserIdSerializer, UserSerializer, RoomSerializer


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
        user = get_object_or_404(MyUser, pk=pk)
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


class RoomAPIView(views.APIView):
    """
    ルームモデルの取得(一覧)・登録APIクラス
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        ルームモデルの取得(一覧)APIに対応するハンドラメソッド
        """

        # モデルオブジェクトの一覧を取得
        room_list = Room.objects.filter(is_private=False)
        # シリアライザオブジェクトを作成
        serializer = RoomSerializer(instance=room_list, many=True)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        ルームモデルの登録APIに対応するハンドラメソッド
        """

        # 子ラリアライザオブジェクトを作成
        serializer = RoomSerializer(data=request.data)
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
        # シリアライザオブジェクトを作成
        serializer = RoomSerializer(instance=room)
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
        serializer = RoomSerializer(instance=room, data=request.data)
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
        serializer = RoomSerializer(
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
        return Response(status=status.HTTP_200_OK)


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
        return Response(status=status.HTTP_200_OK)
