from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('mailing_list/tasks.py', 'r+') as file:
            line = file.readline()
            while line:
                if line.rstrip() == 'from django.utils import timezone':
                    file.truncate(file.tell())
                    break
                line = file.readline()
