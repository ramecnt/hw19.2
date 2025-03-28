from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    """
    A model representing a user.

    Attributes:
        email (str): The user's email address, used as the unique identifier for authentication.
        phone (str): The user's phone number. Optional and must be unique if provided.
        avatar (ImageField): The user's profile picture. Optional.
        country (str): The country of residence of the user. Optional.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=35, verbose_name="Телефон", unique=True, **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=40, verbose_name="Страна", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
