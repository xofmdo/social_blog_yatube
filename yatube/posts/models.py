from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

MAX_LENGTH = 15


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы'
    )
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Описание группы, к которой будет относиться пост'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:MAX_LENGTH]
