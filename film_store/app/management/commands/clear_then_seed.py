from django.core.management.base import BaseCommand
from app.api.seed.seed import download_dataset, start_seeding, clear_db, disable_signals, enable_signals
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear the database then seed it with initial data'

    def handle(self, *args, **kwargs):
        print("Temporary disable signals...")
        disable_signals()
        print('Seeding database...')
        download_dataset()
        cache.clear()
        clear_db()
        start_seeding()
        enable_signals()

