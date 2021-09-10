import jwt
from config import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from api.models import MyUser
from api.serializers import UserSerializer


class MyJWTAuthentication(BaseAuthentication):
    """
    HTTP-Onlyのトークン確認
    """

    def authenticate(self, request):
        JWT = request.COOKIES.get("user_token")
        if not JWT:
            raise exceptions.AuthenticationFailed("No token")
        user = self.decode_jwt(JWT)
        print(user.display_name)  # For Debug
        if user.is_active:
            serializer = UserSerializer(user)
            return (user, serializer.data)
        raise exceptions.AuthenticationFailed("User is not active")

    def decode_jwt(self, JWT):
        try:
            payload = jwt.decode(
                jwt=JWT, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            return MyUser.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Activations link expired")
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        except MyUser.DoesNotExist:
            raise exceptions.AuthenticationFailed("user does not exists")
