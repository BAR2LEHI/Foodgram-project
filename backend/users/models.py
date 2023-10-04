from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodGramUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]

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
    role = models.CharField(
        choices=ROLE_CHOICES,
        blank=True,
        verbose_name='Роль пользователя'
    )
    recipes_count = models.IntegerField(
        default=0,
        verbose_name='Кол-во рецептов'
    )
    is_subscribed = models.BooleanField(
        verbose_name='Подписан ли',
        default=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('username',)
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
