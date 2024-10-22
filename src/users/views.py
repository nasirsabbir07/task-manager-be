from typing import Any, Dict, Optional

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import CustomUserSerializer


# Create your views here.
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        data: Dict[str, Any] = request.data
        email: str = data.get("email")
        password: str = data.get("password")
        first_name: str = data.get("first_name", "")
        last_name: str = data.get("last_name", "")

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        user: CustomUser = CustomUser.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        serializer: CustomUserSerializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        email: str = request.data.get("email")
        password: str = request.data.get("password")
        user: Optional[CustomUser] = authenticate(
            request, email=email, password=password
        )

        if user is not None:
            refresh: RefreshToken = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)}
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
