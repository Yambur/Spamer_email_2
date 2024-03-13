from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('created_at',)