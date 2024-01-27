
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryForm
from .models import Inquiry, Song, SpotifyUser
from django.utils import timezone
from openai import OpenAI
import ast

client = OpenAI(
    api_key="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"
)

# Set up your Spotify app credentials
SPOTIPY_CLIENT_ID = 'edb9962744cb4fb8abb45296c550e7b1'
SPOTIPY_CLIENT_SECRET = '4d03087a56474108a5d7030d4e6ece8d'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify_set_user/'

def search_for_song(song_title, artist_name, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q': f"track:{song_title} artist:{artist_name}",
        'type': 'track',
        'limit': 1,
    }
    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    data = response.json()
    if 'items' in data.get('tracks', {}) and data['tracks']['items']:
        return data['tracks']['items'][0]['uri']
    else:
        return None

def create_the_playlist(songs_arr, access_token, vibe, artists):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    playlist_name = f"{artists[0]}, {artists[1]}, {artists[2]} - {vibe}"
    playlist_desc = "Django practice project."
    user_id = SpotifyUser.objects.get(access_token=access_token).spotify_id

    playlist_data = {
        'name': playlist_name,
        'public': True,
        'description': playlist_desc,
    }

    response = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', headers=headers, json=playlist_data)
    playlist_id = response.json().get('id', '')
    
    track_ids = []
    successful_songs = []

    for song in songs_arr:
        track_id = search_for_song(song[0], song[1], access_token)
        if track_id:
            track_ids.append(track_id)
            successful_songs.append(song)

    requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks', headers=headers, json={'uris': track_ids})
    
    return successful_songs

def connect_to_spotify(request):
    auth_url = f"https://accounts.spotify.com/authorize?client_id={SPOTIPY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIPY_REDIRECT_URI}&scope=playlist-modify-public%20playlist-modify-private&state=123"
    return render(request, 'spotify_playlist/connect_to_spotify.html', {'auth_url': auth_url})

def spotify_set_user(request):
    code = request.GET.get('code')
    token_info = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIPY_REDIRECT_URI,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET,
    }).json()

    access_token = token_info.get('access_token', '')
    
    if access_token:
        user_info = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': f'Bearer {access_token}'}).json()
        user, created = SpotifyUser.objects.get_or_create(
            spotify_id=user_info['id'],
            display_name=user_info['display_name'],
        )
        user.access_token = access_token
        user.save()
        return redirect('inquiries_index', user_pk=user.pk)
    else:
        # Handle error case
        return render(request, 'error_page.html', {'error_message': 'Failed to authenticate with Spotify'})

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
                prompt = (
                    f"I need you to provide 15 songs for a playlist. "
                    f"I'll give you three artists and a 'vibe'. "
                    f"Your response should be an array with 15 subarrays, each containing a song title and artist. "
                    f"For example: [['Song1', 'Artist1'], ['Song2', 'Artist2'], ...]. "
                    f"Please avoid using double quotes within song titles or artist names. "
                    f"If a song title or artist contains an apostrophe, use a backslash before it. "
                    f"Now, the chosen vibe is '{vibe}' and the three artists are '{artist1}', '{artist2}', and '{artist3}'. "
                    f"Ensure the response is formatted as specified, and I'll be using ast.literal_eval to process it."
                )



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
                print(f"\n\n\n this is the generate text{generated_text} \n\n\n")
                data_str = generated_text.strip('"')
                songs = ast.literal_eval(data_str)
                print(f"\n\n\n this is the songs {songs} \n\n\n")

                successful_songs = create_the_playlist(songs, user.access_token, vibe, [artist1, artist2, artist3])

                for song in successful_songs:
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