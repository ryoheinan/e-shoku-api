from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MyUser, Room
from .serializers import UserSerializer, UserListSerializer, RoomSerializer, RoomListSerializer
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import exceptions as jwt_exp
from .utils.auth import MyJWTAuthentication


class TokenObtainView(jwt_views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])
        print(serializer.validated_data)
        res = Response({"status": "success"}, status=status.HTTP_200_OK)
        try:
            res.delete_cookie("user_token")
        except Exception as e:
            print(e)

        res.set_cookie(
            "user_token",
            serializer.validated_data["access"],
            max_age=60 * 30,
            httponly=True,
        )
        res.set_cookie(
            "refresh_token",
            serializer.validated_data["refresh"],
            max_age=60 * 60 * 24 * 90,
            httponly=True,
        )
        return res


class TokenRefresh(jwt_views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])
        res = Response({"status": "success"}, status=status.HTTP_200_OK)
        res.delete_cookie("user_token")
        res.set_cookie(
            "user_token",
            serializer.validated_data["access"],
            max_age=60 * 30,
            httponly=True,
        )
        return res


def refresh_get(request):
    try:
        RT = request.COOKIES["refresh_token"]
        return JsonResponse({"refresh": RT}, safe=False)
    except Exception as e:
        print(e)
        return None


class UserListCreateAPIView(views.APIView):
    """ユーザモデルの取得(一覧)・登録APIクラス"""

    authentication_classes = [MyJWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """ユーザモデルの取得(一覧)APIに対応するハンドラメソッド"""

        # モデルオブジェクトの一覧を取得
        # user_list = MyUser.objects.all()
        # シリアライザオブジェクトを作成
        # serializer = UserSerializer(instance=user_list, many=True)
        # レスポンスオブジェクトを返す
        return Response({"data": "Hi"}, status.HTTP_200_OK)

    """def post(self, request, *args, **kwargs):
        """
    # ユーザモデルの登録APIに対応するハンドラメソッド
    """

        # 子ラリアライザオブジェクトを作成
        serializer = UserSerializer(data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_201_CREATED)
    """


class UserRetrieveUpdateDestroyAPIView(views.APIView):
    """ユーザモデルの取得(詳細)・更新・一部更新・削除APIクラス"""

    def get(self, request, pk, *args, **kwargs):
        """ユーザモデルの取得(詳細)APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = UserSerializer(instance=user)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """ユーザモデルの更新APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = UserSerializer(instance=user, data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """ユーザモデルの一部更新APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
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
        """ユーザモデルの削除APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        user = get_object_or_404(MyUser, pk=pk)
        # モデルオブジェクトを削除
        user.delete()
        # レスポンスオブジェクトを返す
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomListCreateAPIView(views.APIView):
    """ルームモデルの取得(一覧)・登録APIクラス"""

    def get(self, request, *args, **kwargs):
        """ルームモデルの取得(一覧)APIに対応するハンドラメソッド"""

        # モデルオブジェクトの一覧を取得
        room_list = Room.objects.all()
        # シリアライザオブジェクトを作成
        serializer = RoomSerializer(instance=room_list, many=True)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        """ルームモデルの登録APIに対応するハンドラメソッド"""

        # 子ラリアライザオブジェクトを作成
        serializer = RoomSerializer(data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_201_CREATED)


class RoomRetrieveUpdateDestroyAPIView(views.APIView):
    """ルームモデルの取得(詳細)・更新・一部更新・削除APIクラス"""

    def get(self, request, pk, *args, **kwargs):
        """ルームモデルの取得(詳細)APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = RoomSerializer(instance=room)
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """ルームモデルの更新APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
        # シリアライザオブジェクトを作成
        serializer = RoomSerializer(instance=room, data=request.data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを更新
        serializer.save()
        # レスポンスオブジェクトを返す
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """ルームモデルの一部更新APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        room = get_object_or_404(Room, pk=pk)
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
        """ロームモデルの削除APIに対応するハンドラメソッド"""

        # モデルオブジェクトを取得
        room = get_object_or_404(MyUser, pk=pk)
        # モデルオブジェクトを削除
        room.delete()
        # レスポンスオブジェクトを返す
        return Response(status=status.HTTP_204_NO_CONTENT)
