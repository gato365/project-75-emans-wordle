from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
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
            form.save()
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
def game_history(request):
    games = Game.objects.filter(user=request.user).order_by('-date')
    
    game_data = []
    for game in games:
        guesses = Guess.objects.filter(game=game).order_by('sequence_number')
        guess_data = []
        for guess in guesses:
            try:
                time_taken = guess.time.time_taken
            except GuessTime.DoesNotExist:
                time_taken = None
            guess_data.append({
                'word': guess.guess_word,
                'time_taken': time_taken
            })
        
        game_data.append({
            'date': game.date,
            'word': game.word.word,
            'status': game.status,
            'time_played': game.time_played,
            'guesses': guess_data
        })
    
    context = {
        'game_data': game_data,
        'title': 'Game History'  # This will be used in the base.html title block
    }
    return render(request, 'users/game_history.html', context)


