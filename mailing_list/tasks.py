from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from mailing_list.models import Message, Client, Logs
from django.utils import timezone


@shared_task(name='send_mail_1_to_clients')
def send_mail_1_to_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=1)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')


@shared_task(name='send_mail_2_to_clients')
def send_mail_2_to_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=2)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')


@shared_task(name='send_mail_3_to_clients')
def send_mail_3_to_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk=3)
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
