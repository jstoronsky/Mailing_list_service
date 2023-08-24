from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='jstoronsky@test.com',
            first_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        superuser.set_password('Demon6600')
        superuser.save()
