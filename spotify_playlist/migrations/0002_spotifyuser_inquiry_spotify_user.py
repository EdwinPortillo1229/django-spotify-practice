# Generated by Django 5.0 on 2024-01-20 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_playlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='inquiry',
            name='spotify_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='spotify_playlist.spotifyuser'),
        ),
    ]
