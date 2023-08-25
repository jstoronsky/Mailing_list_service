from django_celery_beat.models import PeriodicTask
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        tasks = PeriodicTask.objects.all()
        for task in tasks:
            task.enabled = True
            task.save()
