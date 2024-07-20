import logging
from django.conf import settings
from django.core.management import BaseCommand
from django.apps import apps
from django.db import connection, transaction

from registrar.management.commands.utility.terminal_helper import TerminalHelper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Drops all tables in the database'

    def handle(self, **options):
        """Delete all rows from a list of tables"""

        if settings.IS_PRODUCTION:
            logger.error("clean_tables cannot be run in production")
            return

        self.print_tables()
        logger.info(self.style.WARNING('Dropping all tables...'))
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
        logger.info(self.style.SUCCESS('All tables dropped.'))

    def print_tables(self):
        self.stdout.write(self.style.WARNING('Fetching table names...'))
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            table_names = cursor.fetchall()
            if table_names:
                self.stdout.write(self.style.NOTICE('Tables in the database:'))
                for name in table_names:
                    self.stdout.write(name[0])
            else:
                self.stdout.write('No tables found.')