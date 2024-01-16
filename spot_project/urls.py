from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("landing_page/", include("spotify_playlist.urls")),
    path("admin/", admin.site.urls),
]