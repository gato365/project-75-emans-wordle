from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game, Word, Guess, GuessDetail, Leaderboard
import random
import json



@login_required
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def game_view(request):
    if request.method == "GET":
        context = {
            'key': 'value'
        }
        return render(request, 'wordle/game.html', context)
    elif request.method == "POST":
        return start_game(request)





@login_required
def start_game(request):
    """Start a new game."""
    word = Word.objects.order_by('?').first()
    if not word:
        return JsonResponse({'error': 'No words available'}, status=400)   
    game = Game.objects.create(user=request.user, word=word, status='active')
    return JsonResponse({
        'game_id': game.id,
        'attempts_left': 6,
        'word_length': word.length
    })





@login_required
@require_POST
def submit_guess(request):
    """Handle a guess submission."""
    data = json.loads(request.body)
    game_id = data.get('game_id')
    guess_word = data.get('guess')
    
    game = get_object_or_404(Game, id=game_id, user=request.user)
    
    if game.status != 'active':
        return JsonResponse({'error': 'Game is not active'}, status=400)
    
    correct_word = game.word.word
    feedback = []
    
    for i, letter in enumerate(guess_word):
        if letter == correct_word[i]:
            result = 'correct'
        elif letter in correct_word:
            result = 'present'
        else:
            result = 'absent'
        feedback.append({'letter': letter, 'result': result})
    
    guess = Guess.objects.create(
        game=game,
        guess_word=guess_word,
        sequence_number=game.guess_set.count() + 1
    )
    
    for i, f in enumerate(feedback):
        GuessDetail.objects.create(
            guess=guess,
            position=i,
            letter=f['letter'],
            result=f['result']
        )
    
    game_over = False
    is_win = False
    
    if guess_word == correct_word:
        game.status = 'won'
        game_over = True
        is_win = True
    elif game.guess_set.count() >= 6:
        game.status = 'lost'
        game_over = True
    
    game.save()
    
    if game_over:
        update_leaderboard(request.user, is_win)
    
    return JsonResponse({
        'feedback': feedback,
        'attempts_left': 6 - game.guess_set.count(),
        'game_over': game_over,
        'is_win': is_win,
        'correct_word': correct_word if game_over else None
    })

@login_required
def get_leaderboard(request):
    """Retrieve leaderboard data."""
    leaderboard = Leaderboard.objects.order_by('-score')[:10]
    data = [{'username': entry.user.username, 'score': entry.score} for entry in leaderboard]
    return JsonResponse({'leaderboard': data})

def update_leaderboard(user, is_win):
    """Update the leaderboard after a game."""
    score_change = 1 if is_win else -1
    leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user)
    leaderboard_entry.score += score_change
    leaderboard_entry.save()

@login_required
@require_POST
def update_settings(request):
    """Update user settings."""
    data = json.loads(request.body)
    setting_type = data.get('setting_type')
    value = data.get('value')
    
    Setting.objects.update_or_create(
        user=request.user,
        setting_type=setting_type,
        defaults={'value': value}
    )
    
    return JsonResponse({'status': 'success'})




