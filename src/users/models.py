import datetime
from typing import Any, Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password"""
        if not email:
            raise ValueError("The email field must be set")
        email: str = self.normalize_email(email)
        user: CustomUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str], **extra_fields: Any
    ) -> "CustomUser":
        """Create and save a superuser with the given email and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email instead of username"""

    email: str = models.EmailField(unique=True)
    first_name: str = models.CharField(max_length=30, blank=True)
    last_name: str = models.CharField(max_length=30, blank=True)
    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)
    date_joined: "datetime" = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

    # groups = models.ManyToManyField(
    #     "auth.group",
    #     related_name="customuser_set",
    #     blank=True,
    #     help_text="This groups this user belongs to.",
    #     verbose_name="groups",
    # )

    # user_permissions = models.ManyToManyField(
    #     "auth.permission",
    #     related_name="customuser_set",
    #     blank=True,
    #     help_text="Specific permission for this user.",
    #     verbose_name="user permission",
    # )

    def __str__(self) -> str:
        return self.email
