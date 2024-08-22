from django.core.management.base import BaseCommand
import app.models
import os
from app.api.seed.seed import download_dataset, start_seeding, clear_db, disable_signals, enable_signals
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear the database except superuser'

    def handle(self, *args, **kwargs):
        cache.clear()
