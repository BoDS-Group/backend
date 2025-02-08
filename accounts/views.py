import jwt
import datetime

from django.conf import settings
from django.db import connection
from django.contrib.auth.hashers import check_password 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    permission_classes = []  

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, password FROM auth_user WHERE username = %s", [username])
            row = cursor.fetchone()

        if row is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        user_id, db_username, db_password = row

        if not check_password(password, db_password):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "user_id": user_id,
            "username": db_username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({"token": token}, status=status.HTTP_200_OK)
