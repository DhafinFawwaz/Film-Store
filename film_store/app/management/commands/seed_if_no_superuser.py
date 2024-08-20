from django.core.management.base import BaseCommand
from app.models import GeneralUser
import os
from app.api.seed.seed import download_dataset, start_seeding, clear_db

class Command(BaseCommand):
    help = 'Seed the database with initial data if no superuser exists'

    def handle(self, *args, **kwargs):
        if not GeneralUser.objects.filter(is_superuser=True).exists():
            print('Seeding database...')
            download_dataset()
            start_seeding()


