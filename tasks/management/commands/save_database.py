from django.core.management.base import BaseCommand, CommandError
from django.core import management
import datetime

class Command(BaseCommand):
    help = 'Save database as fixture and CSV'

    def handle(self, *args, **options):
        # Get the current date and time as a string
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d-%H-%M-%S")

        # Save the fixture file using the current date in the file name
        fixture_filename = f"db_fixture_{date_str}.json"
        filepath = f"database_backups/{fixture_filename}"

        try:
            with open(filepath, 'w') as f:
                management.call_command('dumpdata', '--indent=4', stdout=f)
                print("this worked!")
        except Exception as e:
            print("it didn't work!!!")
            raise CommandError(f"Error saving fixture: {e}")

        self.stdout.write(self.style.SUCCESS(f"Successfully saved fixture ({fixture_filename})"))

