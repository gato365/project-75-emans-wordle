from django.db import models
from users.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)

class Word(models.Model):
    word = models.CharField(max_length=255)
    length = models.IntegerField()

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess_word = models.CharField(max_length=255)
    sequence_number = models.IntegerField()

class GuessDetail(models.Model):
    guess = models.ForeignKey(Guess, on_delete=models.CASCADE)
    position = models.IntegerField()
    letter = models.CharField(max_length=1)
    result = models.CharField(max_length=50)

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setting_type = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
