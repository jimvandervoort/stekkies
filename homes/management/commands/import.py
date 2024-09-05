import csv

from django.core.management.base import BaseCommand

from homes.models import Home


def update_home(home, row):
    home.address = row['Address']
    home.city = row['City']
    home.website = row['Website']
    home.photo = row['Photo']
    home.price = float(row['Price'].replace(',', ''))
    home.rooms = int(row['Rooms'])
    home.surface = int(row['Surface'])
    home.balcony = row['Balcony'].lower() == 'true'
    home.bath = row['Bath'].lower() == 'true'
    home.furnished = row['Furnished'].lower() == 'true'
    home.garden = row['Garden'].lower() == 'true'
    home.description = row['Description']
    home.bedrooms = int(row['Bedrooms'])
    home.save()


def create_home(row):
    Home.objects.create(
        url=row['URL'],
        address=row['Address'],
        city=row['City'],
        website=row['Website'],
        photo=row['Photo'],
        price=float(row['Price'].replace(',', '')),
        rooms=int(row['Rooms']),
        surface=int(row['Surface']),
        balcony=row['Balcony'].lower() == 'true',
        bath=row['Bath'].lower() == 'true',
        furnished=row['Furnished'].lower() == 'true',
        garden=row['Garden'].lower() == 'true',
        description=row['Description'],
        bedrooms=int(row['Bedrooms']),
        lat=0,
        lon=0,
    )


class Command(BaseCommand):
    help = 'Import homes'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV path')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                home = Home.objects.filter(url=row['URL']).first()
                if home:
                    update_home(home, row)
                    continue

                try:
                    create_home(row)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing home on row {reader.line_num}: {e}'))
                    continue

        self.stdout.write(self.style.SUCCESS(f'Processed {reader.line_num} homes'))
