from django.shortcuts import render

# Create your views here.




def game(request):
    return render(request, 'wordle/game.html')