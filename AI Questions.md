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
