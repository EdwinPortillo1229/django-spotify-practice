# spot_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spotify_playlist/', include('spotify_playlist.urls')),
]
