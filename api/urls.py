from django.urls import path
from . import views

urlpatterns = [
    # ユーザモデルの取得(一覧)・登録
    path('users/', views.UserAPIView.as_view(), name='users'),
    # ユーザモデルの取得(詳細)・更新・一部更新・削除
    path('users/<pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),
    # ルームモデルの取得(一覧)・登録
    path('rooms/', views.RoomAPIView.as_view(), name='rooms'),
    # ルームモデルの取得(詳細)・更新・一部更新・削除
    path('rooms/<pk>/', views.RoomRetrieveUpdateDestroyAPIView.as_view()),
    # ルーム参加API
    path('rooms/join/<pk>/', views.RoomJoinAPIView.as_view()),
    # ルーム参加キャンセルAPI
    path('rooms/leave/<pk>/', views.RoomLeaveAPIView.as_view()),
]
