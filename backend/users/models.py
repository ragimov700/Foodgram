from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, db_index=True,
                              verbose_name='email')
    username = models.CharField(max_length=150, unique=True,
                                verbose_name='юзернейм',
                                validators=(RegexValidator(
                                    regex=r'^[\w.@+-]+\Z',
                                    message='Некорректное значение'),))
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-pk',)

    def __str__(self):
        return self.email


class Subscriber(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='subscriber',
                             verbose_name='подписчик')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='author', verbose_name='автор')

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
        constraints = (models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_subscribe'),)

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
