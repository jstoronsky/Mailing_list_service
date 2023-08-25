from django_celery_beat.models import PeriodicTask
from mailing_list.models import SettingsMailing
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        tasks = PeriodicTask.objects.all()
        settings_ = SettingsMailing.objects.all()
        for task in tasks:
            task.enabled = False
            task.save()
        for seti in settings_:
            seti.status = 'Не активна'
            seti.save()
