import csv
from django.core.management.base import BaseCommand
from django.db import connections




class Command(BaseCommand):
    help = 'Save transactions table as CSV'

    def handle(self, *args, **options):
        connection = connections['default']

       # Save the CSV file using the current date in the file name
        csv_filename = "transactions.csv"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions_transaction")
            with open(f"database_backups/{csv_filename}", 'w') as f:
                writer = csv.writer(f)
                writer.writerow([col[0] for col in cursor.description])
                writer.writerows(cursor)

        self.stdout.write(self.style.SUCCESS(f"Successfully saved CSV file ({csv_filename}"))