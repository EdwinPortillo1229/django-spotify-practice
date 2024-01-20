# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryForm
from .models import Inquiry
from .models import Song
from .models import SpotifyUser
from django.utils import timezone
from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ast

client = OpenAI(
    api_key="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"
)

# Set up your Spotify app credentials
SPOTIPY_CLIENT_ID = '3040ec93145a41f58a74663e82bf1015'
SPOTIPY_CLIENT_SECRET = '6e176a0e9f4342d7aa9358d016111fa9'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify_set_user/'
sp = spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="playlist-modify-public playlist-modify-private")


def connect_to_spotify(request):
    auth_url = sp.get_authorize_url()
    return render(request, 'spotify_playlist/connect_to_spotify.html', {'auth_url': auth_url})

def spotify_set_user(request):
    code = request.GET.get('code')
    token_info = sp.get_access_token(code)
    access_token = token_info['access_token']
    spot = spotipy.Spotify(auth=access_token)
    user_info = spot.me()
    print(user_info)

    user, created = SpotifyUser.objects.get_or_create(
        spotify_id=user_info['id'],
        display_name=user_info['display_name'],
    )
    user.access_token = access_token
    user.save()

    # Redirect to inquiries_index with the user's primary key as a parameter
    return redirect('inquiries_index', user_pk=user.pk)

def inquiries_index(request, user_pk):
    user = get_object_or_404(SpotifyUser, pk=user_pk)
    inquiries = Inquiry.objects.filter(spotify_user=user)
    return render(request, 'spotify_playlist/inquiries_index.html', {'user': user, 'inquiries': inquiries})

def create_inquiry(request, user_pk):
        user = get_object_or_404(SpotifyUser, pk=user_pk)
        if request.method == 'POST':
            form = InquiryForm(request.POST)
            if form.is_valid():
                # Create an Inquiry instance using form data
                artist1 = form.cleaned_data['artist1']
                artist2 = form.cleaned_data['artist2']
                artist3 = form.cleaned_data['artist3']
                vibe = form.cleaned_data['vibe']
                
                inquiry = Inquiry(
                    artist1=artist1,
                    artist2=artist2,
                    artist3=artist3,
                    vibe=vibe,
                    date_of_inquiry = timezone.now(),
                    spotify_user = user
                )
                inquiry.save()
                prompt = (f"Listen. I need you to return something very specific to me, "
                    f"you can be misinterpreting this because I am using you in my code, "
                    f"and if you send me the wrong thing it will break everything. "
                    f"I am going to provide you three artists and a 'vibe' -- "
                    f"I want you to give me 15 songs (5 each of the 3 artists) that match "
                    f"the vibe given to the best of your ability. "
                    f"For your answer, I want only an array. "
                    f"It is important you DO NOT SAY ANYTHING ELSE BEYOND THIS ARRAY. "
                    f"Within the array, I want an array for each song, "
                    f"and I want it to be first the song title, then the artist. "
                    f"For example, if I asked for Michael Jackson, The Beatles, and The Weeknd "
                    f"and the vibe is chill, I would want something along the lines of "
                    f"[['Beat It', 'Michael Jackson'], ['Yellow Submarine', 'The Beatles'], "
                    f"['Starboy', 'The Weeknd']]. Please please please only give me the array, nothing else. "
                    f"Now chosen vibe is '{vibe}' and the three artists are '{artist1}', "
                    f"'{artist2}', and '{artist3}'. "
                    f"Don't just give me their most popular songs, and make sure they match the vibe of '{vibe}' "
                    f"for the last time, please give me 15 songs in an array within a string. dont convert to json to anything. straight up array within a string so i can convert the string to array")

                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-4",
                )                
                generated_text = response.choices[0].message.content
                data_str = generated_text.strip('"')
                songs = ast.literal_eval(data_str)

                for song in songs:
                    song = Song(
                        song_title = song[0],
                        artist_name = song[1],
                        inquiry = inquiry
                    )
                    song.save()

                return redirect('inquiries_index', user_pk=user_pk)
        else:
            form = InquiryForm()

        return render(request, 'spotify_playlist/create_inquiry.html', {'form': form, 'user': user})

def inquiry_detail(request, user_pk, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    user = get_object_or_404(SpotifyUser, pk=user_pk)
    songs = Song.objects.filter(inquiry=inquiry)
    return render(request, 'spotify_playlist/inquiry_detail.html', {'inquiry': inquiry, 'songs': songs, 'user': user})