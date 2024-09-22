from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game, Word, Guess, GuessTime, UserGame, get_current_wordle_date
from collections import Counter
from django.utils import timezone
import json
import logging
import traceback
logger = logging.getLogger(__name__)
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.conf import settings





@login_required
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def game_view(request):
    if request.method == "GET":
        today_word = Word.get_word_for_today()
        if not today_word:
            return render(request, 'wordle/game.html', {'error': 'No word available for today.'})
        
        # Check if user has already played today
        if UserGame.objects.filter(user=request.user, date_played=get_current_wordle_date()).exists():
            return render(request, 'wordle/game.html', {'error': 'You have already played today.'})
        
        context = {
            'word': today_word.word,
            'next_game_time': (datetime.combine(get_current_wordle_date() + timedelta(days=1), settings.WORDLE_RESET_TIME)).isoformat(),
            # Add any other context data you need
        }
        return render(request, 'wordle/game.html', context)
    elif request.method == "POST":
        return start_game(request)




def start_game(request):
    """Start a new game."""
    try:
        today = timezone.now().date()
        today_word = Word.get_word_for_today()
        
        logger.debug(f"Today's date: {today}")
        logger.debug(f"Today's word: {today_word}")
        
        if not today_word:
            return JsonResponse({'error': 'No word available for today'}, status=400)
        
        # Check if user has already played today
        if UserGame.objects.filter(user=request.user, date_played=today).exists():
            return JsonResponse({'error': 'You have already played today'}, status=400)
        
        game = Game.objects.create(
            user=request.user,
            word=today_word,  # Use the Word object directly, not its ID
            status='active',
            time_played=0
        )
        UserGame.objects.create(user=request.user, date_played=today)
        
        logger.debug(f"Created game: {game}")
        
        return JsonResponse({
            'game_id': game.id,
            'attempts_left': 6
        })
    except Exception as e:
        logger.error(f"Error in start_game: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def submit_guess(request):
    """Handle a guess submission."""
    data = json.loads(request.body)
    game_id = data.get('game_id')
    guess_word = data.get('guess')
    time_taken = data.get('time_taken')
    
    game = get_object_or_404(Game, id=game_id, user=request.user)
    
    if game.status != 'active':
        return JsonResponse({'error': 'Game is not active'}, status=400)
    
    correct_word = game.word.word
    

    logger.debug(f"Game {game_id}: Correct word is {correct_word}, guess is {guess_word}")
    feedback = [{'letter': letter, 'result': 'absent'} for letter in guess_word]
    


    # Count the occurrences of each letter in the correct word and the guess
    correct_letter_counts = Counter(correct_word)
    guess_letter_counts = Counter(guess_word)
    
    # First pass: Mark correct letters
    for i, letter in enumerate(guess_word):
        if letter == correct_word[i]:
            feedback[i]['result'] = 'correct'
            correct_letter_counts[letter] -= 1
            guess_letter_counts[letter] -= 1
    
    # Second pass: Mark present letters
    for i, letter in enumerate(guess_word):
        if feedback[i]['result'] == 'absent' and correct_letter_counts[letter] > 0:
            feedback[i]['result'] = 'present'
            correct_letter_counts[letter] -= 1
            guess_letter_counts[letter] -= 1
    
    guess = Guess.objects.create(
        game=game,
        guess_word=guess_word,
        sequence_number=game.guess_set.count() + 1
    )

    GuessTime.objects.create(
        guess=guess,
        time_taken=time_taken
    )
    
    game.time_played += time_taken
    game.save()
    
  
    
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
    

    
    return JsonResponse({
        'feedback': feedback,
        'attempts_left': 6 - game.guess_set.count(),
        'game_over': game_over,
        'is_win': is_win,
        'correct_word': correct_word if game_over else None
    })



@login_required
@require_POST
def update_guess_times(request):
    data = json.loads(request.body)
    game_id = data.get('game_id')
    guess_times = data.get('guess_times')
    
    game = get_object_or_404(Game, id=game_id, user=request.user)
    guesses = game.guess_set.all().order_by('sequence_number')
    
    for guess, time_taken in zip(guesses, guess_times):
        GuessTime.objects.update_or_create(
            guess=guess,
            defaults={'time_taken': time_taken}
        )
    
    game.time_played = sum(guess_times)
    game.save()
    
    return JsonResponse({'status': 'success'})


@login_required
@require_POST
def update_game_time(request):
    data = json.loads(request.body)
    game_id = data.get('game_id')
    time_taken = data.get('time_taken')
    
    game = get_object_or_404(Game, id=game_id, user=request.user)
    game.time_played = time_taken
    game.save()
    
    return JsonResponse({'status': 'success'})





