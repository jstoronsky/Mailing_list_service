from django.core.management import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join('mailing_list', 'tasks.py')
        with open(path, 'r+') as file:
            line = file.readline()
            while line:
                if line.rstrip() == 'from django.utils import timezone':
                    file.truncate(file.tell())
                    break
                line = file.readline()
