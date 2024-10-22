from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


# Create your views here.
class TaskListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    # *Get tasks for logged in users
    def get(self, request):
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    # * create a new task
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    # *retrieve a task
    def get(self, request, pk):
        task: Task = get_object_or_404(Task, pk=pk, owner=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    # *Update a task
    def put(self, request, pk):
        task: Task = get_object_or_404(Task, pk=pk, owner=request.user)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    # * Delete a task
    def delete(self, request, pk):
        task: Task = get_object_or_404(Task, pk=pk, owner=request.user)
        task.delete
        return Response(status=status.HTTP_204_NO_CONTENT)
