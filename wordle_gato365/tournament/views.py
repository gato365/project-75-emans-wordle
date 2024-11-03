from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views import View
import logging
logger = logging.getLogger(__name__)


from .models import Tournament, TournamentTeam, TournamentWord, TeamWordAttempt
from .forms import (
    TeamRegistrationForm, 
    TournamentWordForm, 
    TeamWordAttemptForm,
    QuickJoinTournamentForm
)


# def register_team(request, tournament_id):
#     tournament = get_object_or_404(Tournament, id=tournament_id)
    
#     if request.method == 'POST':
#         form = TeamRegistrationForm(request.POST, tournament=tournament)
#         if form.is_valid():
#             team = form.save(commit=False)
#             team.tournament = tournament
#             team.save()
            
         
                
#             messages.success(request, "Team registered successfully!")
#             return redirect('tournament:lobby', pk=tournament.pk)
#     else:
#         form = TeamRegistrationForm(tournament=tournament)
    
#     return render(request, 'tournament/register_team.html', {'form': form})





class TournamentListView(LoginRequiredMixin, ListView):
    """Display all active tournaments"""
    model = Tournament
    template_name = 'tournament/tournament_list.html'
    context_object_name = 'tournaments'
    
    def get_queryset(self):
        return Tournament.objects.filter(
            is_active=True,
            end_time__gt=timezone.now()
        ).order_by('start_time')

class TournamentLobbyView(LoginRequiredMixin, DetailView):
    """Tournament lobby where teams wait for tournament to start"""
    model = Tournament
    template_name = 'tournament/tournament_lobby.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        user_team = TournamentTeam.objects.filter(
            tournament=tournament
        ).first()
        
        context.update({
            'user_team': user_team,
            'teams': TournamentTeam.objects.filter(tournament=tournament),
            'is_started': tournament.start_time <= timezone.now(),
            'is_ended': tournament.end_time <= timezone.now(),
            'time_to_start': (tournament.start_time - timezone.now()).total_seconds() if tournament.start_time > timezone.now() else 0
        })
        logger.error(f"User team: {user_team}")
        return context

class TeamRegistrationView(LoginRequiredMixin, CreateView):
    """Handle team registration for a tournament"""
    model = TournamentTeam
    form_class = TeamRegistrationForm
    template_name = 'tournament/team_registration.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tournament'] = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        return kwargs
    
    def form_valid(self, form):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        ## error log
        

        # Check if tournament registration is still open
        # if tournament.start_time <= timezone.now():
        #     messages.error(self.request, "Tournament registration is closed.")
        #     return redirect('tournament:tournament_list')
        
        # Create team
        team = form.save(commit=False)
        team.tournament = tournament
        team.save()

        
        
 
        
        messages.success(self.request, f"Team {team.name} successfully registered!")
        return redirect('tournament:tournament_lobby', pk=tournament.pk)

class TournamentGameView(LoginRequiredMixin, DetailView):
    """Main game view for tournament"""
    model = TournamentTeam
    template_name = 'tournament/tournament_game.html'
    
    def get_object(self):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        return get_object_or_404(
            TournamentTeam,
            tournament=tournament
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        tournament = team.tournament
        
        # Get current word attempt
        current_word = TournamentWord.objects.filter(
            tournament=tournament,
            order_number=team.current_word_index + 1
        ).first()
        
        current_attempt = TeamWordAttempt.objects.filter(
            team=team,
            tournament_word=current_word
        ).first()
        
        context.update({
            'current_word': current_word,
            'current_attempt': current_attempt,
            'attempts_left': 6 - (current_attempt.attempts_used if current_attempt else 0),
            'words_completed': team.current_word_index,
            'total_words': TournamentWord.objects.filter(tournament=tournament).count(),
            'time_remaining': (tournament.end_time - timezone.now()).total_seconds() if tournament.end_time > timezone.now() else 0
        })
        return context

@login_required
def submit_guess(request, tournament_pk):
    """Handle word guess submission"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    team = get_object_or_404(
        TournamentTeam,
        tournament_id=tournament_pk
    )
    tournament = team.tournament
    
    # Validate tournament is ongoing
    if not tournament.is_ongoing():
        return JsonResponse({'error': 'Tournament is not active'}, status=400)
    
    form = TeamWordAttemptForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors}, status=400)
    
    current_word = TournamentWord.objects.filter(
        tournament=tournament,
        order_number=team.current_word_index + 1
    ).first()
    
    if not current_word:
        return JsonResponse({'error': 'No more words available'}, status=400)
    
    # Get or create attempt
    attempt, created = TeamWordAttempt.objects.get_or_create(
        team=team,
        tournament_word=current_word,
        defaults={'start_time': timezone.now()}
    )
    
    # Check attempts limit
    if attempt.attempts_used >= 6:
        return JsonResponse({'error': 'Maximum attempts reached'}, status=400)
    
    # Process guess
    guess = form.cleaned_data['guess']
    attempt.attempts_used += 1
    
    # Check if guess is correct
    if guess == current_word.word:
        attempt.is_solved = True
        attempt.completion_time = timezone.now()
        attempt.score = calculate_word_score(attempt)
        team.total_score += attempt.score
        team.current_word_index += 1
    
    attempt.save()
    team.save()
    
    return JsonResponse({
        'correct': attempt.is_solved,
        'attempts_left': 6 - attempt.attempts_used,
        'score': attempt.score if attempt.is_solved else 0,
        'feedback': generate_word_feedback(guess, current_word.word)
    })

class LeaderboardView(LoginRequiredMixin, ListView):
    """Tournament leaderboard display"""
    model = TournamentTeam
    template_name = 'tournament/leaderboard.html'
    context_object_name = 'teams'
    
    def get_queryset(self):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['tournament_pk'])
        return TournamentTeam.objects.filter(
            tournament=tournament
        ).order_by('-total_score', 'completion_time')

@login_required
def end_tournament(request, tournament_pk):
    """Handle early tournament completion"""
    team = get_object_or_404(
        TournamentTeam,
        tournament_id=tournament_pk
    )
    
    if not team.is_completed:
        team.is_completed = True
        team.completion_time = timezone.now() - team.tournament.start_time
        team.save()
        
        messages.success(request, "Tournament completed successfully!")
    
    return redirect('tournament:leaderboard', tournament_pk=tournament_pk)

# Helper functions
def calculate_word_score(attempt):
    """Calculate score for a word based on attempts and time"""
    base_score = 100
    attempt_penalty = (attempt.attempts_used - 1) * 10
    time_taken = (attempt.completion_time - attempt.start_time).total_seconds()
    time_penalty = int(time_taken / 10)  # 1 point per 10 seconds
    
    return max(0, base_score - attempt_penalty - time_penalty)

def generate_word_feedback(guess, correct_word):
    """Generate Wordle-style feedback for a guess"""
    feedback = []
    correct_word = list(correct_word)
    
    # First pass: mark correct letters
    for i, letter in enumerate(guess):
        if i < len(correct_word) and letter == correct_word[i]:
            feedback.append('correct')
        elif letter in correct_word:
            feedback.append('present')
        else:
            feedback.append('absent')
    
    return feedback