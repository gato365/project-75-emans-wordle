from django.shortcuts import render

# Create your views here.



def wordle_game(request):
    return render(request, 'wordle/index.html')


def game(request):
    return render(request, 'wordle/game.html')