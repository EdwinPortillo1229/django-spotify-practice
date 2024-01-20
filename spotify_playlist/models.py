# spotify_playlist/models.py

from django.db import models

class SpotifyUser(models.Model):
    access_token = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)

class Inquiry(models.Model):
    artist1 = models.CharField(max_length=255)
    artist2 = models.CharField(max_length=255)
    artist3 = models.CharField(max_length=255)
    date_of_inquiry = models.DateTimeField('date published')
    vibe = models.CharField(max_length=255)
    spotify_user = models.ForeignKey(SpotifyUser, related_name='inquiries', on_delete=models.CASCADE, default=None, null=True)


class Song(models.Model):
    song_title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    inquiry = models.ForeignKey(Inquiry, related_name='songs', on_delete=models.CASCADE)
