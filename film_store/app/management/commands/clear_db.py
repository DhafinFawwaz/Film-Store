from django.core.management.base import BaseCommand
import app.models
import os
from app.api.seed.seed import download_dataset, start_seeding, clear_db

class Command(BaseCommand):
    help = 'Clear the database except superuser'

    def handle(self, *args, **kwargs):
        clear_db()
