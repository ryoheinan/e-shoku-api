import time
import jwt
from config.settings import SECRET_KEY
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from datetime import datetime, timedelta


from app.models import CustomUser


class NormalAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request._request.POST.get("username")
        password = request._request.POST.get("password")
        user_obj = CustomUser.objects.filter(username=username).first()
        if not user_obj:
            raise exceptions.AuthenticationFailed('認証失敗')
        elif not check_password(password, user_obj.password):
            raise exceptions.AuthenticationFailed('パスワードがあってません')
        token = generate_jwt(user_obj)
        return (token, None)

    def authenticate_header(self, request):
        pass


def generate_jwt(user):
    dt = datetime.now() + timedelta(days=1)
    result = jwt.encode({
        "username": user.username,
        "exp": dt.utcfromtimestamp(dt.timestamp())
    }, SECRET_KEY)
    return result
