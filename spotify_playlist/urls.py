# urls.py in spotify_playlist app

from django.urls import path
from .views import create_inquiry, success_page

urlpatterns = [
    path('create_inquiry/', create_inquiry, name='create_inquiry'),
    path('success_page/', success_page, name='success_page'),
]
