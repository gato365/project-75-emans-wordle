"""
URL configuration for wordle_gato365 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from wordle import views as wordle_views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', user_views.home),
    path('home/', user_views.home, name='home'),
    path('about/', user_views.about, name='about'),
    path('leaderboardlist/',user_views.leaderboardlist, name='leaderboardlist'),

    path('stats/',user_views.stats, name='stats'),
    path('register/', user_views.register, name='register'),
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    
    path('start_game/', wordle_views.start_game, name='start_game'),
    path('game/', wordle_views.game_view, name='game'),
    path('logout/', user_views.CustomLogoutView.as_view(), name='logout')
   
]  + static(settings.STATIC_URL)