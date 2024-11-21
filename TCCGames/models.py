from django.db import models
from django.contrib.auth.models import AbstractUser

class PlayerScore:
    def __init__(self, user_id, points=0, level=1):
        self.user_id = user_id
        self.points = points
        self.level = level

    def calculate_level(self):
        self.level = self.points // 100 + 1

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )