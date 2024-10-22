# tasks/urls.py
from django.urls import path

from .views import TaskDetailAPI, TaskListCreateAPI

urlpatterns: list[path] = [
    path("tasks", TaskListCreateAPI.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailAPI.as_view(), name="task-detail"),
]
