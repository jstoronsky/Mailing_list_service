from django_celery_beat.models import PeriodicTask
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        PeriodicTask.objects.all().delete()
