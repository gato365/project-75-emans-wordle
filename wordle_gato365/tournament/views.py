from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tournament, TournamentTeam
from django.shortcuts import render, redirect
from django.contrib import messages



class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'tournament/tournament_list.html'
    context_object_name = 'tournaments'
    
    def get_queryset(self):
        return Tournament.objects.filter(is_active=True)




def register_team(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST, tournament=tournament)
        if form.is_valid():
            team = form.save(commit=False)
            team.tournament = tournament
            team.save()
            
            # Process team members
            emails = form.cleaned_data['member_emails']
            for email in emails:
                user = User.objects.get(email=email)
                TeamMember.objects.create(team=team, user=user)
                
            messages.success(request, "Team registered successfully!")
            return redirect('tournament:lobby', pk=tournament.pk)
    else:
        form = TeamRegistrationForm(tournament=tournament)
    
    return render(request, 'tournament/register_team.html', {'form': form})