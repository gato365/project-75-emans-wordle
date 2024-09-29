from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    # path('post/<int:pk>/', name='post-detail'),
    # path('about/', views.about, name='user-about'),
]