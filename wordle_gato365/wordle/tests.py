from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Game, Word

class WordleViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.word = Word.objects.create(word='HELLO', date='2023-10-01')
        self.game = Game.objects.create(user=self.user, word=self.word, status='won', time_played=300)

    def test_game_creation(self):
        self.assertEqual(self.game.user, self.user)
        self.assertEqual(self.game.word, self.word)
        self.assertEqual(self.game.status, 'won')
        self.assertEqual(self.game.time_played, 300)

    def test_general_game_history_view(self):
        # Test redirection for non-logged in user
        response = self.client.get(reverse('game_history'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('game_history')}")

        # Test for logged in user
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('game_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'HELLO')  # Assuming the word is displayed in game history

    def test_badges_view(self):
        # Test redirection for non-logged in user
        response = self.client.get(reverse('badges'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('badges')}")

        # Test for logged in user
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('badges'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        # Add more assertions based on what should be in the badges page

    def test_summary_of_all_games_view(self):
        # Test redirection for non-logged in user
        response = self.client.get(reverse('summary_of_all_games'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('summary_of_all_games')}")

        # Test for logged in user
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('summary_of_all_games'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        # Add more assertions based on what should be in the summary page

    def test_all_games_played_view(self):
        # Test redirection for non-logged in user
        response = self.client.get(reverse('all_games_played'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('all_games_played')}")

        # Test for logged in user
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('all_games_played'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'HELLO')  # Assuming the word is displayed in all games played




## Test Badges
## Test Summary of all games
## Test All games played
## Test Game history