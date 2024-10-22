from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "description", "completed", "created_at", "owner"]
        read_only_fields = ["id", "owner", "created_at"]
