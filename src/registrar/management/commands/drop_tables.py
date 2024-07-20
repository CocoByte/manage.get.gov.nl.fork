import logging
from django.conf import settings
from django.core.management import BaseCommand
from django.apps import apps
from django.db import transaction

from registrar.management.commands.utility.terminal_helper import TerminalHelper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Drops all tables in the database'

    def handle(self, **options):
        """Delete all rows from a list of tables"""

        if settings.IS_PRODUCTION:
            logger.error("clean_tables cannot be run in production")
            return

        self.stdout.write(self.style.WARNING('Dropping all tables...'))
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
        self.stdout.write(self.style.SUCCESS('All tables dropped.'))