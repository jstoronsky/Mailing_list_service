from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from mailing_list.models import Message
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        message = Message.objects.get(pk=2)
        current_time = timezone.now()
        if message.time_to_start <= current_time:
            PeriodicTask.objects.create(name=f'mailing list_{message}', task='send_mail_2_to_clients',
                                        interval=IntervalSchedule.objects.get(every=message.custominterval.every,
                                                                              period=message.custominterval.period),
                                        start_time=timezone.now(), expires=message.time_to_end)
        elif message.time_to_start > current_time:
            PeriodicTask.objects.create(name=f'mailing list{message}', task='send_mail_2_to_clients',
                                        interval=IntervalSchedule.objects.get(every=message.custominterval.every,
                                                                              period=message.custominterval.period),
                                        start_time=message.time_to_start, expires=message.time_to_end)
