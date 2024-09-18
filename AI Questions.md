Question 1:

OK so this is not working. So I want to have a deeper understanding.

Main Goal: So What I want, is for a user to click on Game History and their game history to display.
ddsThis is what I believe happens:
    1) User clicks on Game History (given they are logged in)
    2) The user is redirected to the Game History page (an html page)
Issue 1: My current issue is that game_history.html is a block of html code and I do not have a content region in base.html to display the game history. Is that correct? If so, how do I create a content region in base.html to display the game history?
Issue 2: How is the views in my user directory connected to the game history html page in the templates directory?
    3) Somehow the views.py file in the user directory is connected to the game_history.html page in the templates directory.
    4) The views.py goes to the database and retrieves the game history for the user.

Please address my issues and critique my understanding. Thank you.

---------------------------------------------------------------------------------------------------------
Question 2:
a) Regarding my game history issue, it worked. I have the table history that has the following columns:
 - Date	
 - Word	
 - Status	
 - Time Played	
 - Guesses

b) I would like to change it to be the following:
 - Date	
 - Word	
 - Number of Guesses
 - If Did you win	
 - Average time per guess	
 - Total time on guess

c) My models look like this:
```python
class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    ## amount of time the game has been played
    time_played = models.IntegerField(default=0)

class Word(models.Model):
    word = models.CharField(max_length=255)
    date_used = models.DateField(null=True) 
    

    def __str__(self):
        return self.word

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess_word = models.CharField(max_length=255)
    sequence_number = models.IntegerField()

class GuessTime(models.Model):
    guess = models.OneToOneField(Guess, on_delete=models.CASCADE, related_name='time')
    time_taken = models.FloatField()  # Time in secon
```

I also want to deck out my game history page to have a modern look with Bootstrap 



---------------------------------------------------------------------------------------------------------
Question 3:
So I want to advanve the game history table to have one main tab named "Badges" then 2 more tabs names "Summary of All games" and "All Games Played"

The previous request allowed me to get all games played now I want to work on the summary of all games. 

a) I know I need to modify the urls.py to have more paths. 
b) I know the views.py within users need 3 more functions: general, badges, summary_of_all_games, and all_games_played (already done)[is this correct]
c) I will need to have 3 more html pages in the templates directory: badges.html, summary_of_all_games.html, and all_games_played.html
d) I would like to have a empty badge page that I will work on soon.
---------------------------------------------------------------------------------------------------------

Question 4:
Thank you but my user name is showing up but none of the games in their respective table. How do I manage this issue?
- I think the issue is in the views in that it is not getting the games for the user correctly. Here is the relevant code:
```python

from django.db.models import Avg, Count, Sum
from wordle.models import Game, Guess, GuessTime

@login_required
def general_game_history(request):
    return render(request, 'users/game_history.html')

@login_required
def badges(request):
    # This will be implemented later
    return render(request, 'users/badges.html')

@login_required
def summary_of_all_games(request):
    user = request.user
    games = Game.objects.filter(user=request.user)

    summary = {
        'total_games': games.count(),
        'games_won': games.filter(status='won').count(),
        'average_guesses': Guess.objects.filter(game__user=request.user).values('game').annotate(guess_count=Count('id')).aggregate(Avg('guess_count'))['guess_count__avg'],
        'total_time_played': games.aggregate(Sum('time_played'))['time_played__sum'],
        'average_time_per_game': games.aggregate(Avg('time_played'))['time_played__avg'],
    }
    if summary['total_games'] > 0:
        win_rate = (summary['games_won'] / summary['total_games']) * 100
    else:
        win_rate = 0

    context = {
        'summary': summary,
        'win_rate': win_rate,
        'user': user
    }
    return render(request, 'users/summary_of_all_games.html', context)




@login_required
def all_games_played(request):
    games = Game.objects.filter(user=request.user).order_by('-date')
    
    game_data = []
    for game in games:
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
        'game_data': game_data
    }
    
    return render(request, 'users/all_games_played.html', context)

```

---------------------------------------------------------------------------------------------------------
Question 5:
This information will be gathered in their form
For each user I would like to know more information about them.
- If they are a student, i want to know their 
    - Graduating class: 2024, 2025, 2026, 2027, 2028 as options
    - College membership:  Orfalea College of Business,  Bailey College of Science and Mathematics, College of Agriculture, Food and Environmental Sciences, College of Architecture and Environmental, College of Liberal Arts, College of Engineering
    - Major: textbox
- If they are a faculty member, I want to know their
    - College membership:  Orfalea College of Business,  Bailey College of Science and Mathematics, College of Agriculture, Food and Environmental Sciences, College of Architecture and Environmental, Not Applicable

Here is my registraytionhtml page:
```
{% extends "users/base.html" %}
{% load crispy_forms_tags %}
{% block content1 %}
    <div class="content-section">
        <form method="POST" autocomplete="off">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Join Today</legend>
                {{ form|crispy }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Sign Up</button>
            </div>
        </form>
        <div class="border-top pt-3">
            <small class="text-muted">
                Already Have An Account? <a class="ml-2" href="#">Sign In</a>
            </small>
        </div>
    </div>
{% endblock content1 %}
```

Here is my views
```python
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
```

I doubt I need to change anythring from my urls.py file.



------------------------------------------------------------------------------------


Question 6:

So here is my Words Model
```
class Word(models.Model):
    word = models.CharField(max_length=255)
    date_used = models.DateField(null=True) 
```

I want the users to only play this game once a day in which everyone gets the same word. I would like to have only one game played per day for 70. 
Should I preload the table with the dates and based on day the word that corresponds to the day would show up?
What else do I need to change?