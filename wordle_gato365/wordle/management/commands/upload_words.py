import csv
from django.core.management.base import BaseCommand
from wordle.models import Word

class Command(BaseCommand):
    help = 'Upload words from a CSV file into the Word model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing words')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                word = row[0]
                Word.objects.create(word=word)
                self.stdout.write(self.style.SUCCESS(f'Successfully added word: {word}'))