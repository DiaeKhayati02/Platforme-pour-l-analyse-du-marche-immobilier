import csv
from django.core.management.base import BaseCommand
from myapp.models import Records

class Command(BaseCommand):
    help = 'Load records from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load records...'))
        path = options['csv_file']
        with open(path, newline='', encoding='Windows-1252') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Records(
                    Type_de_bien=row['Type_de_bien'],
                    Zone=row['Zone'],
                    Name=row['Name'],
                    Action_commerciale=row['Action_commerciale'],
                    Nom_et_Prenom=row['Nom_et_Prenom'],
                    Superficie=float(row['Superficie']),
                    Disponibilite=row['Disponibilite']
                )
                record.save()
        self.stdout.write(self.style.SUCCESS('Successfully loaded all records.'))
