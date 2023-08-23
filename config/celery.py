from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Moscow')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')
# Load task modules from all registered Django apps.
# Celery Beat tasks registration
# app.conf.beat_schedule = {'Send_mail_to_Client':
#                           {'task': 'mailing_list.task.my_scheduled_job1', 'schedule': 30.0}}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')