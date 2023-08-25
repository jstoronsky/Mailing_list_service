from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException
from django_celery_beat.models import PeriodicTask
from mailing_list.models import Message, Logs, SettingsMailing
from django.utils import timezone


@shared_task(name='send_mail_24_to_clients')
def send_mail_to_24_clients():
    message = Message.objects.get(pk=24)
    clients = SettingsMailing.objects.get(message=message).clients.all()
    clients_mails = [client.email for client in clients]
    try:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, clients_mails)
        message.settingsmailing.status = 'Активна'
        message.settingsmailing.save(update_fields=['status'])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_Купон в Джанго_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'Не активна'
            message.settingsmailing.save(update_fields=['status'])
    except SMTPException:
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Не отправлено')
        task = PeriodicTask.objects.get(task=f'send_mail_Купон в Джанго')
        task.enabled = False
        task.save()
        message.settingsmailing.status = 'Не активна'
        message.settingsmailing.save(update_fields=['status'])

