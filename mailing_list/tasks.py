from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask

from mailing_list.models import Message, Client, Logs
from django.utils import timezone


@shared_task(name='send_mail_6_to_clients')
def send_mail_6_to_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=6)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        message.settingsmailing.status = 'IN_PROCESS'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_{message}_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'OVER'
            message.settingsmailing.save(update_fields=['status'])


@shared_task(name='send_mail_7_to_clients')
def send_mail_to_7_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=7)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        message.settingsmailing.status = 'IN_PROCESS'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_{message}_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'OVER'
            message.settingsmailing.save(update_fields=['status'])


@shared_task(name='send_mail_8_to_clients')
def send_mail_to_8_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=8)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(),
                            status='Отправлено')
        message.settingsmailing.status = 'IN_PROCESS'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_Рассылкапосылка_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'OVER'
            message.settingsmailing.save(update_fields=['status'])


@shared_task(name='send_mail_9_to_clients')
def send_mail_to_9_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=9)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        message.settingsmailing.status = 'IN_PROCESS'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_Посылаю вам каштаны_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'OVER'
            message.settingsmailing.save(update_fields=['status'])


@shared_task(name='send_mail_12_to_clients')
def send_mail_to_12_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=12)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        message.settingsmailing.status = 'IN_PROCESS'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_Вести с Камчатки_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'OVER'
            message.settingsmailing.save(update_fields=['status']) 


@shared_task(name='send_mail_15_to_clients')
def send_mail_to_15_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=15)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        message.settingsmailing.status = 'IN_PROCESS'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_Рассссыылка_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'OVER'
            message.settingsmailing.save(update_fields=['status']) 


