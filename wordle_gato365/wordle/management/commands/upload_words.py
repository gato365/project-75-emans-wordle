import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from wordle.models import Word

class Command(BaseCommand):
    help = 'Update date_used for existing words in the Word model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing words and dates')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = row['word'].strip()
                date_str = row['date'].strip()
                date = parse_date(date_str)
                
                if not date:
                    self.stdout.write(self.style.WARNING(f'Invalid date format for word {word}: {date_str}. Skipping.'))
                    continue
                
                try:
                    # Try to get existing word
                    word_obj = Word.objects.filter(word=word).first()
                    
                    if word_obj:
                        # Update the date
                        word_obj.date = date
                        word_obj.save()
                        self.stdout.write(self.style.SUCCESS(f'Updated date for word: {word} to {date}'))
                    else:
                        # Create a new word if it doesn't exist
                        Word.objects.create(word=word, date=date)
                        self.stdout.write(self.style.SUCCESS(f'Created new word: {word} with date: {date}'))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to update/create word: {word}. Error: {str(e)}'))

