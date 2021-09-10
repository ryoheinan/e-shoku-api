from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', views.TokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ユーザモデルの取得(一覧)・登録
    path('users/', views.UserListCreateAPIView.as_view()),
    # ユーザモデルの取得(詳細)・更新・一部更新・削除
    path('users/<pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),
    # ルームモデルの取得(一覧)・登録
    path('room/', views.RoomListCreateAPIView.as_view()),
    # ルームモデルの取得(詳細)・更新・一部更新・削除
    path('room/<pk>/', views.RoomRetrieveUpdateDestroyAPIView.as_view()),
]
