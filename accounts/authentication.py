import jwt
from django.conf import settings
from django.db import connection
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        user_id = payload.get("user_id")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username FROM auth_user WHERE id = %s", [user_id])
            row = cursor.fetchone()
        if row is None:
            raise exceptions.AuthenticationFailed("User not found")

        user = {
            "id": row[0],
            "username": row[1]
        }

        return (user, token)
