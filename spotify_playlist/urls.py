# urls.py in spotify_playlist app

from django.urls import path
from .views import create_inquiry, inquiries_index

urlpatterns = [
    path('create_inquiry/', create_inquiry, name='create_inquiry'),
    path('inquiries_index/', inquiries_index, name='inquiries_index'),
]
