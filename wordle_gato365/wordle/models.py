from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()


class Word(models.Model):
    word = models.CharField(max_length=255)
    date = models.DateField()

    @classmethod
    def get_word_for_today(cls):
        today = timezone.now().date()
        try:
            return cls.objects.filter(date=today).first()
        except ObjectDoesNotExist:
            return None

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
