import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    code = ''.join([str(secrets.token_urlsafe(5))])
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    verify_code = models.CharField(max_length=10, default=code, verbose_name='Код проверки')
    is_verified = models.BooleanField(default=False, verbose_name='Проверка верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []