from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model: "CustomUser" = CustomUser
        fields: list[str] = ["id", "email", "first_name", "last_name", "date_joined"]
