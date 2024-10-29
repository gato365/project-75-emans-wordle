from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    access_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    max_team_size = models.IntegerField(default=4)
    min_team_size = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.name} - {self.start_time.date()}"

    def is_ongoing(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

class TournamentTeam(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(default=0)
    completion_time = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['name', 'tournament']

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"

class TeamMember(models.Model):
    team = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = ['team', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

class TournamentWord(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    word = models.CharField(max_length=5)  # Assuming 5-letter words like regular Wordle
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    order_number = models.IntegerField()
    points = models.IntegerField(default=100)

    class Meta:
        unique_together = ['tournament', 'order_number']
        ordering = ['order_number']

    def __str__(self):
        return f"{self.word} ({self.difficulty}) - Round {self.order_number}"

class TeamWordAttempt(models.Model):
    team = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE)
    tournament_word = models.ForeignKey(TournamentWord, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    completion_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    success = models.BooleanField(default=False)
    attempts_used = models.IntegerField(default=0)
    is_solved = models.BooleanField(default=False)

    class Meta:
        unique_together = ['team', 'tournament_word']

    def __str__(self):
        return f"{self.team.name} - Word {self.tournament_word.order_number}"