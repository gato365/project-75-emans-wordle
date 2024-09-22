from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Sum
from wordle.models import Game, Guess, GuessTime
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'You just logged out.')
        return super().dispatch(request, *args, **kwargs)

CustomUser = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.user_type == 'faculty_staff':
                user.graduating_class = 'not_applicable'
            user.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            if user.user_type == 'faculty_staff':
                user.graduating_class = 'not_applicable'
            user.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)




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


def badges_view(request):
    user = request.user

    games = Game.objects.filter(user=user)
    games_played = request.user.games_played
    
    context = {
        'games_played': games_played,
    }
    return render(request, 'users/badges.html', context)



# You can keep these separate views if needed, or remove them if not used
@login_required
def summary_of_all_games(request):
    return general_game_history(request)

@login_required
def all_games_played(request):
    return general_game_history(request)




@login_required
def badges_view(request):
    user_badges = UserBadge.objects.filter(user=request.user).values_list('badge_name', flat=True)
    badges = [
        {
            "name": "First Word",
            "description": "Awarded for completing the first Wordle puzzle.",
            "image": "wordle/images/first_word_badge.png",
            "unlocked": request.user.games_played > 0
        },
        {
            "name": "Perfect Week",
            "description": "Solve 7 consecutive puzzles (one week) without missing a day.",
            "image": "wordle/images/seven_days_badge.png",
            "unlocked": False  # You'll need to implement the logic for this
        },
        {
            "name": "Streak Master",
            "description": "Maintain a streak of 14 days or more.",
            "image": "wordle/images/fourteen_days_badge.png",
            "unlocked": False  # You'll need to implement the logic for this
        },
        {
            "name": "Vocabulary Virtuoso",
            "description": "Correctly guess 5 words that are considered advanced vocabulary.",
            "image": "wordle/images/vocab_badge.png",
            "unlocked": False  # You'll need to implement the logic for this
        },
        {
            "name": "Speed Racer",
            "description": "Solve a puzzle in under 2 minutes.",
            "image": "wordle/images/speed_racer_badge.png",
            "unlocked": False  # You'll need to implement the logic for this
        },
        {
            "name": "Lucky Guess",
            "description": "Solve a puzzle on the first try (this is rare and partly luck-based).",
            "image": "wordle/images/lucky_guess_badge.png",
            "unlocked": False  # You'll need to implement the logic for this
        },
    ]

    return render(request, 'wordle/badges.html', {'badges': badges})