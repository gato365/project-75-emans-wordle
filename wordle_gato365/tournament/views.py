from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tournament, TournamentTeam

class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'tournament/tournament_list.html'
    context_object_name = 'tournaments'
    
    def get_queryset(self):
        return Tournament.objects.filter(is_active=True)

# Add other views as needed...