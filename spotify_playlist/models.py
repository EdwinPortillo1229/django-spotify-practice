# spotify_playlist/models.py

from django.db import models

class Inquiry(models.Model):
    artist1 = models.CharField(max_length=255)
    artist2 = models.CharField(max_length=255)
    artist3 = models.CharField(max_length=255)
    date_of_inquiry = models.DateTimeField('date published')
    vibe = models.CharField(max_length=255)

class Song(models.Model):
    song_title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    inquiry = models.ForeignKey(Inquiry, related_name='songs', on_delete=models.CASCADE)
