from django.contrib import admin
from .models import Tournament, TournamentTeam,  TournamentWord, TeamWordAttempt

admin.site.register(Tournament)
admin.site.register(TournamentTeam)
admin.site.register(TournamentWord)
admin.site.register(TeamWordAttempt)
