from django.core.management.base import BaseCommand
from app.api.seed.seed import download_dataset, start_seeding, clear_db

class Command(BaseCommand):
    help = 'Clear the database then seed it with initial data'

    def handle(self, *args, **kwargs):
        print('Seeding database...')
        download_dataset()
        clear_db()
        start_seeding()

