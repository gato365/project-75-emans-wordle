from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Sum
from wordle.models import Game, Guess, GuessTime

# Create your views here.

def leaderboardlist(request):
    leaderboard_data = []
    for i in range(1, 11):
        player_data = {
            'rank': i,
            'player': f'Player {i}',
            'games_played': 10 + i,
            'games_won': 8 + i,
            'win_percentage': (8 + i) / (10 + i) * 100,
            'average_guesses': 4 + (i % 3),
            'best_word': f'Word{i}'
        }
        leaderboard_data.append(player_data)
    
    context = {
        'leaderboard_data': leaderboard_data
    }
    return render(request, 'users/leaderboardlist.html', context)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'You just logged out.')
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'faculty':
                user.graduating_class = None
                user.major = None
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES,
                                   instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html',context)






def home(request):
    context = {
        'title': 'Home Page',
        # Add other context variables here
    }
    return render(request, 'users/home.html', context)


def about(request):
    return render(request, 'users/about.html')

def leaderboardlist(request):
    return render(request, 'users/leaderboardlist.html')



def stats(request):
    return render(request, 'users/stats.html')







@login_required
def general_game_history(request):
    user = request.user
    games = Game.objects.filter(user=user)

    summary = {
        'total_games': games.count(),
        'games_won': games.filter(status='won').count(),
        'average_guesses': Guess.objects.filter(game__user=user).values('game').annotate(guess_count=Count('id')).aggregate(Avg('guess_count'))['guess_count__avg'],
        'total_time_played': games.aggregate(Sum('time_played'))['time_played__sum'],
        'average_time_per_game': games.aggregate(Avg('time_played'))['time_played__avg'],
    }

    if summary['total_games'] > 0:
        win_rate = (summary['games_won'] / summary['total_games']) * 100
    else:
        win_rate = 0

    game_data = []
    for game in games.order_by('-date'):
        guesses = Guess.objects.filter(game=game)
        guess_times = GuessTime.objects.filter(guess__game=game)
        
        game_data.append({
            'date': game.date,
            'word': game.word.word,
            'num_guesses': guesses.count(),
            'won': game.status == 'won',
            'avg_time_per_guess': guess_times.aggregate(Avg('time_taken'))['time_taken__avg'] or 0,
            'total_time': game.time_played
        })

    context = {
        'summary': summary,
        'win_rate': win_rate,
        'user': user,
        'game_data': game_data
    }
    
    return render(request, 'users/game_history.html', context)

@login_required
def badges(request):
    # This will be implemented later
    return render(request, 'users/badges.html')

# You can keep these separate views if needed, or remove them if not used
@login_required
def summary_of_all_games(request):
    return general_game_history(request)

@login_required
def all_games_played(request):
    return general_game_history(request)