from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
import pytz
from datetime import datetime, time, timedelta



def get_current_wordle_date():
    """Get the date for the current Wordle game in PST."""
    now = timezone.now().astimezone(settings.WORDLE_TIMEZONE)
    today_reset = now.replace(hour=settings.WORDLE_RESET_TIME.hour, 
                              minute=settings.WORDLE_RESET_TIME.minute, 
                              second=settings.WORDLE_RESET_TIME.second, 
                              microsecond=0)
    
    if now < today_reset:
        return (today_reset - timedelta(days=1)).date()
    return today_reset.date()

User = get_user_model()


class Word(models.Model):
    word = models.CharField(max_length=255)
    date = models.DateField()


    @classmethod
    def get_word_for_today(cls):
        today = get_current_wordle_date()
        return cls.objects.filter(date=today).first()

    def __str__(self):
        return f"{self.word} - {self.date}"

class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    ## amount of time the game has been played
    time_played = models.IntegerField(default=0)



class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess_word = models.CharField(max_length=255)
    sequence_number = models.IntegerField()

class GuessTime(models.Model):
    guess = models.OneToOneField(Guess, on_delete=models.CASCADE, related_name='time')
    time_taken = models.FloatField()  # Time in secon


# You might want to add a UserGame model to track plays
class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_played = models.DateField()

    class Meta:
        unique_together = ['user', 'date_played']


