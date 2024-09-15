from django.db import models
from users.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)

    date = models.DateField(auto_now_add=True)

class Word(models.Model):
    word = models.CharField(max_length=255)
    date_used = models.DateField(null=True) 
    

    def __str__(self):
        return self.word

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess_word = models.CharField(max_length=255)
    sequence_number = models.IntegerField()

