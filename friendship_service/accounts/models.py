from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )