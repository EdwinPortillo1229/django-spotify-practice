# spot_project/urls.py

from django.contrib import admin
from django.urls import path, include
from spotify_playlist.views import connect_to_spotify


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', connect_to_spotify, name='connect_to_spotify'),
    path('', include('spotify_playlist.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
