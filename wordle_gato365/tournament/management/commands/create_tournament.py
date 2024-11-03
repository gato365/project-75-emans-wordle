from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from tournament.models import Tournament, TournamentWord
import csv
import pytz

class Command(BaseCommand):
    help = 'Create tournament and load words from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing tournament words')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        tz = pytz.timezone('America/Los_Angeles')
        
        # Create tournament
        ## Now
        start_time = tz.localize(datetime.now()) #tz.localize(datetime(2024, 11, 8, 10, 0))
        end_time = tz.localize(datetime(2024, 11, 8, 12, 0))

        try:
            # Create the tournament
            tournament = Tournament.objects.create(
                name="The 2nd Dragon",
                start_time=start_time,
                end_time=end_time,
                access_code="Dragon Breaths Fire",
                is_active=True,
                max_team_size=4,
                min_team_size=2
            )
            
            # Read and load words
            with open(csv_file, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    TournamentWord.objects.create(
                        tournament=tournament,
                        word=row['word'],
                        difficulty=row['difficulty'],
                        order_number=int(row['order_number']),
                        points=int(row['points'])
                    )
            
            # Verify word counts
            easy_count = TournamentWord.objects.filter(tournament=tournament, difficulty='easy').count()
            medium_count = TournamentWord.objects.filter(tournament=tournament, difficulty='medium').count()
            hard_count = TournamentWord.objects.filter(tournament=tournament, difficulty='hard').count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created tournament: {tournament.name}\n'
                    f'Loaded words:\n'
                    f'- Easy: {easy_count}\n'
                    f'- Medium: {medium_count}\n'
                    f'- Hard: {hard_count}\n'
                    f'Total words: {easy_count + medium_count + hard_count}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Failed to create tournament or load words. Error: {str(e)}'
                )
            )