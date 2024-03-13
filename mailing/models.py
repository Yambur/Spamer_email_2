from django.db import models
from django.db.models.functions import datetime
from config import settings

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Клиент для рассылки"""
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name', 'first_name')


class Message(models.Model):
    """Сообщение для рассылки"""
    title = models.CharField(max_length=100, verbose_name='Тема сообщения', default='Без темы')
    text = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title',)


class Mailing(models.Model):
    """Информация о рассылки"""
    STATUS_CHOICES = [
        ('created', 'Создано'),
        ('started', 'Запущено'),
        ('completed', 'Завершено'),
    ]

    PERIOD_CHOICES = [
        ('once', '1 раз'),
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    start_point = models.DateTimeField(verbose_name='Начать рассылку', default=datetime.datetime.now)
    stop_point = models.DateTimeField(verbose_name='Завершить рассылку', default=datetime.datetime.now)
    period = models.CharField(max_length=20, verbose_name='Периодичность', choices=PERIOD_CHOICES, default='once')
    status = models.CharField(max_length=20, verbose_name='Статус', choices=STATUS_CHOICES, default='created')

    client = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE, **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Владелец', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активная')

    def __str__(self):
        return f'{self.start_point} {self.period} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('set_is_active', 'Изменить период'),
        ]


class Log(models.Model):
    """Логи для рассылки"""
    LOG_CHOICES = [
        (True, 'Успешно'),
        (False, 'Ошибка')
    ]
    attempt_time = models.DateTimeField(verbose_name='Последняя попытка', **NULLABLE)
    attempt_status = models.CharField(max_length=10, verbose_name='Статус попытки', choices=LOG_CHOICES, default=True)
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE, **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.attempt_time}, статус : {self.attempt_status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
