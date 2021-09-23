from django.urls import path
from . import views

urlpatterns = [
    # ユーザモデルの取得(一覧)・登録
    path('users/', views.UserListCreateAPIView.as_view(), name='users'),
    # ユーザモデルの取得(詳細)・更新・一部更新・削除
    path('users/<pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),
    # ルームモデルの取得(一覧)・登録
    path('rooms/', views.RoomListCreateAPIView.as_view(), name='rooms'),
    # ルームモデルの取得(詳細)・更新・一部更新・削除
    path('rooms/<pk>/', views.RoomRetrieveUpdateDestroyAPIView.as_view()),
]
