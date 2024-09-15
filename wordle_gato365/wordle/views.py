from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game, Word, Guess
from collections import Counter
import json
import logging
logger = logging.getLogger(__name__)



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
    
    # word = Word.objects.order_by('?').first()
    ## select a word from the database that is the first word in the database
    word = Word.objects.first()
    if not word:
        return JsonResponse({'error': 'No words available'}, status=400)   
    game = Game.objects.create(user=request.user, word=word, status='active')
    return JsonResponse({
        'game_id': game.id,
        'attempts_left': 6
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




