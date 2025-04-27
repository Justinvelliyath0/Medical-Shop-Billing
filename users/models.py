from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ("ADMIN", "Admin"),
    ("STAFF", "Staff"),
    ("INV_MANAGER", "InvManager"),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={"unique": "This username is already taken."},
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.username
