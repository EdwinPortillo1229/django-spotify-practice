# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryForm
from .models import Inquiry
from .models import Song
from django.utils import timezone
from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ast

client = OpenAI(
    api_key="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"
)

# Set up your Spotify app credentials
SPOTIPY_CLIENT_ID = 'ddeddc01708d4387a7e10aff1a62b065'
SPOTIPY_CLIENT_SECRET = '285a252875b8496bbd6664514aab9b60'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/inquiries_index/'

def create_inquiry(request):
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
                    date_of_inquiry = timezone.now()
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

                return redirect('inquiries_index')
        else:
            form = InquiryForm()

        return render(request, 'spotify_playlist/create_inquiry.html', {'form': form})

def inquiries_index(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'spotify_playlist/inquiries_index.html', {'inquiries': inquiries})

def inquiry_detail(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    songs = Song.objects.filter(inquiry=inquiry)
    return render(request, 'spotify_playlist/inquiry_detail.html', {'inquiry': inquiry, 'songs': songs})