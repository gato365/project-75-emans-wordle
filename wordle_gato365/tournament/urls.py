from django.urls import path
from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.TournamentListView.as_view(), name='tournament_list'),
    path('<int:pk>/lobby/', views.TournamentLobbyView.as_view(), name='tournament_lobby'),
    path('<int:tournament_pk>/join/', views.TeamRegistrationView.as_view(), name='tournament_join'),
    path('<int:tournament_pk>/game/', views.TournamentGameView.as_view(), name='tournament_game'),
    path('<int:tournament_pk>/submit/', views.submit_guess, name='submit_guess'),
    path('<int:tournament_pk>/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('<int:tournament_pk>/end/', views.end_tournament, name='end_tournament'),
]