# tournament/api.py
from rest_framework import viewsets

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    
    @action(detail=True, methods=['post'])
    def submit_guess(self, request, pk=None):
        # Handle guess submission
        pass
    
    @action(detail=True, methods=['get'])
    def current_word(self, request, pk=None):
        # Get current word for team
        pass