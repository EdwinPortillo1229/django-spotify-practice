# spot_project/urls.py

from django.contrib import admin
from django.urls import path, include
from spotify_playlist.views import inquiries_index  # Import the inquiries_index view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inquiries_index, name='inquiries_index'),
    path('', include('spotify_playlist.urls')),  # Include the app's URLs with an empty path
]
