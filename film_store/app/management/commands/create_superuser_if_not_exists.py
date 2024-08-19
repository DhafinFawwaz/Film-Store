from django.core.management.base import BaseCommand
from app.models import GeneralUser
import os

class Command(BaseCommand):
    help = 'Create an admin if does not exist'

    def handle(self, *args, **kwargs):
        if not GeneralUser.objects.filter(is_superuser=True).exists():
            GeneralUser.objects.create_superuser(
                username=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
                password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123'),
                email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@email.com'),
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))

