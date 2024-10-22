import datetime

from django.db import models

from users.models import CustomUser


# Create your models here.
class Task(models.Model):
    tirle: str = models.CharField(max_length=100)
    description: str = models.TextField()
    completed: bool = models.BooleanField(default=False)
    owner: "CustomUser" = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tasks"
    )
    created_at: "datetime" = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
