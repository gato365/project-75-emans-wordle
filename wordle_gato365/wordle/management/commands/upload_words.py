import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from wordle.models import Word
from django.db.models import Q

class Command(BaseCommand):
    help = 'Delete specific rows, update date_used for existing words, and add new words to the Word model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing words and dates')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Delete specific rows
        Word.objects.filter(
            Q(word="peppy", date="2024-10-02") |
            Q(word="yummy", date="2024-10-03")
        ).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted specified rows'))

        # Read CSV and prepare data
        words_to_update = []
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = row['word'].strip()
                date_str = row['date'].strip()
                date = parse_date(date_str)
                
                if not date:
                    self.stdout.write(self.style.WARNING(f'Invalid date format for word {word}: {date_str}. Skipping.'))
                    continue
                
                words_to_update.append((word, date))

        # Sort the words by date
        words_to_update.sort(key=lambda x: x[1])

        # Update or create words in order
        for word, date in words_to_update:
            try:
                word_obj, created = Word.objects.update_or_create(
                    word=word,
                    defaults={'date': date}
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new word: {word} with date: {date}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated date for word: {word} to {date}'))
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to update/create word: {word}. Error: {str(e)}'))