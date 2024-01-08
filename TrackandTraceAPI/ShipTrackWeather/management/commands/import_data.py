import csv
from django.core.management.base import BaseCommand
from ShipTrackWeather.models import Shipment, Article


class Command(BaseCommand):
    """
    Django management command to import data from a CSV file to the database.
    """
    help: str = 'Import data from CSV file to database'

    def handle(self, *args, **options):
        """
        Handles the importing of data from the CSV file to the database.

        Reads data from 'data.csv' and creates Shipment and Article objects in the database.
        """
        file_path = 'data.csv'

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                shipment: Shipment = Shipment.objects.create(
                    tracking_number=row['tracking_number'],
                    carrier=row['carrier'],
                    sender_address=row['sender_address'],
                    receiver_address=row['receiver_address'],
                    status=row['status']
                )

                Article.objects.create(
                    shipment=shipment,
                    article_name=row['article_name'],
                    article_quantity=row['article_quantity'],
                    article_price=row['article_price'],
                    SKU=row['SKU']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
