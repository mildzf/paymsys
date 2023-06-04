import csv
import os
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Save client table as CSV'

    def handle(self, *args, **options):
        connection = connections['default']

        # Create the database_backups directory if it does not exist
        backup_dir = 'database_backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Save the CSV file using the current date in the file name
        csv_filename = "clients.csv"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM clients_client")
            with open(os.path.join(backup_dir, csv_filename), 'w') as f:
                writer = csv.writer(f)
                writer.writerow([col[0] for col in cursor.description])
                writer.writerows(cursor)

        self.stdout.write(self.style.SUCCESS(f"Successfully saved CSV file ({csv_filename}"))



