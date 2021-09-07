"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # ユーザモデルの取得(一覧)・登録
    path('app/users/', views.UserListCreateAPIView.as_view()),
    # ユーザモデルの取得(詳細)・更新・一部更新・削除
    path('app/users/<pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view()),
    # ルームモデルの取得(一覧)・登録
    path('app/room/', views.RoomListCreateAPIView.as_view()),
    # ルームモデルの取得(詳細)・更新・一部更新・削除
    path('app/room/<pk>/', views.RoomRetrieveUpdateDestroyAPIView.as_view()),
]
