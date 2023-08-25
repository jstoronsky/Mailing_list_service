from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException
from django_celery_beat.models import PeriodicTask
from mailing_list.models import Message, Logs, SettingsMailing
from django.utils import timezone
