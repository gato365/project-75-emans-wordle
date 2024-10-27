from django.urls import path
from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.TournamentListView.as_view(), name='tournament_list'),
    path('join/<int:pk>/', views.TournamentJoinView.as_view(), name='tournament_join'),
    path('game/<int:pk>/', views.TournamentGameView.as_view(), name='tournament_game'),
    path('leaderboard/<int:pk>/', views.LeaderboardView.as_view(), name='leaderboard'),
]