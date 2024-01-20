# urls.py in spotify_playlist app

from django.urls import path
from .views import create_inquiry, inquiries_index, inquiry_detail, connect_to_spotify

urlpatterns = [
    path('create_inquiry/', create_inquiry, name='create_inquiry'),
    path('inquiries_index/', inquiries_index, name='inquiries_index'),
    path('inquiry_detail/<int:pk>/', inquiry_detail, name='inquiry_detail'),
    path('connect_to_spotify/', connect_to_spotify, name='connect_to_spotify'),
]
