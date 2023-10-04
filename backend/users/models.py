from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodGramUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('username',)
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
