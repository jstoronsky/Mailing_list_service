from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from mailing_list.models import Message
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        message = Message.objects.get(pk=1)
        current_time = timezone.now()
        if message.time_to_start <= current_time:
            PeriodicTask.objects.create(name=f'mailing list_{message}', task='send_mail_1_to_clients',
                                        interval=IntervalSchedule.objects.get(every=message.custominterval.every,
                                                                              period=message.custominterval.period),
                                        start_time=timezone.now(), expires=message.time_to_end)
        elif message.time_to_start > current_time:
            PeriodicTask.objects.create(name=f'mailing list{message}', task='send_mail__1_to_clients',
                                        interval=IntervalSchedule.objects.get(every=message.custominterval.every,
                                                                              period=message.custominterval.period),
                                        start_time=message.time_to_start, expires=message.time_to_end)
    # def handle(self, *args, **options):
    #     messages = Message.objects.all()
    #     current_time = timezone.now()
    #     for message in messages:
    #         if message.time_to_start <= current_time:
    #             PeriodicTask.objects.create(name=f'mailing list_{message}', task='send_mail_to_client',
    #                                         interval=IntervalSchedule.objects.get(every=message.custominterval.every,
    #                                                                               period=message.custominterval.period),
    #                                         start_time=timezone.now(), expires=message.time_to_end)
    #         elif message.time_to_start > current_time:
    #             PeriodicTask.objects.create(name=f'mailing list{message}', task='send_mail_to_client',
    #                                         interval=IntervalSchedule.objects.get(every=message.custominterval.every,
    #                                                                               period=message.custominterval.period),
    #                                         start_time=message.time_to_start, expires=message.time_to_end)
