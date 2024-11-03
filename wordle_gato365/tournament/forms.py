from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Tournament, TournamentTeam, TournamentWord, TeamWordAttempt

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_time', 'end_time', 'access_code', 'max_team_size', 'min_team_size', 'is_active']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        min_team_size = cleaned_data.get('min_team_size')
        max_team_size = cleaned_data.get('max_team_size')

        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("End time must be after start time.")
            
            if (end_time - start_time).total_seconds() > 7200:  # 2 hours in seconds
                raise ValidationError("Tournament duration cannot exceed 2 hours.")

        if min_team_size and max_team_size:
            if min_team_size > max_team_size:
                raise ValidationError("Minimum team size cannot be greater than maximum team size.")
            if min_team_size < 2:
                raise ValidationError("Minimum team size must be at least 2.")
            if max_team_size > 4:
                raise ValidationError("Maximum team size cannot exceed 4.")

class TeamRegistrationForm(forms.ModelForm):
    access_code = forms.CharField(max_length=20, widget=forms.PasswordInput)
    member_emails = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Specify username (one per line, between 2-4 members, make it up...)"
    )

    class Meta:
        model = TournamentTeam
        fields = ['name']

    def __init__(self, *args, tournament=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament = tournament

    def clean_access_code(self):
        access_code = self.cleaned_data.get('access_code')
        if self.tournament and access_code != self.tournament.access_code:
            raise ValidationError("Invalid tournament access code.")
        return access_code

    def clean_member_emails(self):
        emails = self.cleaned_data.get('member_emails').strip().split('\n')
        emails = [email.strip().lower() for email in emails if email.strip()]
        
        # Validate email count
        if len(emails) < self.tournament.min_team_size:
            raise ValidationError(f"At least {self.tournament.min_team_size} team members required.")
        if len(emails) > self.tournament.max_team_size:
            raise ValidationError(f"Maximum {self.tournament.max_team_size} team members allowed.")

     

   
        return emails

class TournamentWordForm(forms.ModelForm):
    class Meta:
        model = TournamentWord
        fields = ['word', 'difficulty', 'order_number', 'points']
        widgets = {
            'word': forms.TextInput(attrs={'maxlength': 5}),
        }

    def clean_word(self):
        word = self.cleaned_data.get('word')
        if word:
            if len(word) != 5:
                raise ValidationError("Word must be exactly 5 letters long.")
            if not word.isalpha():
                raise ValidationError("Word must contain only letters.")
        return word.upper()

class TeamWordAttemptForm(forms.ModelForm):
    guess = forms.CharField(max_length=5, min_length=5)

    class Meta:
        model = TeamWordAttempt
        fields = []  # We'll handle the other fields in the view

    def clean_guess(self):
        guess = self.cleaned_data.get('guess', '').strip().upper()
        if not guess.isalpha():
            raise ValidationError("Guess must contain only letters.")
        if len(guess) != 5:
            raise ValidationError("Guess must be exactly 5 letters.")
        return guess



# Quick join form for testing/development
class QuickJoinTournamentForm(forms.Form):
    tournament = forms.ModelChoiceField(
        queryset=Tournament.objects.filter(is_active=True),
        empty_label="Select a tournament"
    )
    team_name = forms.CharField(max_length=100)
    access_code = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        tournament = cleaned_data.get('tournament')
        access_code = cleaned_data.get('access_code')
        team_name = cleaned_data.get('team_name')

        if tournament and access_code:
            if access_code != tournament.access_code:
                raise ValidationError("Invalid tournament access code.")

            # Check if team name is already taken in this tournament
            if TournamentTeam.objects.filter(tournament=tournament, name=team_name).exists():
                raise ValidationError("Team name already exists in this tournament.")

        return cleaned_data