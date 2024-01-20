# spotify_playlist/urls.py

from django.urls import path
from .views import create_inquiry

urlpatterns = [
    # Other URL patterns
    path('create_inquiry/', create_inquiry, name='create_inquiry'),
]
