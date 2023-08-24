from django.db import models
from django_celery_beat.models import IntervalSchedule

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='e-mail клиента')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    middle_name = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    commentary = models.TextField(verbose_name='комментарий')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='добавил клиента')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model, ):
    header = models.CharField(max_length=300, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержание')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создал рассылку')

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Logs(models.Model):
    SENT = "Отправлено"
    NO_SENT = "Не отправлено"

    STATUS_CHOICES = [
        (SENT, "Отправлено"),
        (NO_SENT, "Не отправлено"),
    ]
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='рассылка')
    datetime_of_attempt = models.DateTimeField(verbose_name='время попытки')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='статус попытки')

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'


class SettingsMailing(IntervalSchedule):
    CREATED = "Создана"
    IN_PROCESS = 'Идёт рассылка'
    OVER = "Завершена"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (IN_PROCESS, 'Идёт рассылка'),
        (OVER, "Завершена"),
    ]
    message = models.OneToOneField('Message', on_delete=models.CASCADE, verbose_name='рассылка')
    time_to_start = models.DateTimeField(verbose_name='время начала рассылки(формат следующий: YYYY-MM-DD HH:MM:SS)', **NULLABLE)
    time_to_end = models.DateTimeField(verbose_name='время завершения рассылки(формат следующий: YYYY-MM-DD HH:MM:SS)', **NULLABLE)
    status = models.CharField(default=CREATED, max_length=50, choices=STATUS_CHOICES, verbose_name='статус рассылки')

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылок'
