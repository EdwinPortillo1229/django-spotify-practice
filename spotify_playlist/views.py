# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryForm
from .models import Inquiry
from .models import Song
from django.utils import timezone

artist_names = ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5", "Artist6", "Artist7", "Artist8", "Artist9", "Artist10", "Artist11", "Artist12", "Artist13", "Artist14", "Artist15"]
song_titles = ["Song1", "Song2", "Song3", "Song4", "Song5", "Song6", "Song7", "Song8", "Song9", "Song10", "Song11", "Song12", "Song13", "Song14", "Song15"]

def create_inquiry(request):
        if request.method == 'POST':
            form = InquiryForm(request.POST)
            if form.is_valid():
                # Create an Inquiry instance using form data
                inquiry = Inquiry(
                    artist1=form.cleaned_data['artist1'],
                    artist2=form.cleaned_data['artist2'],
                    artist3=form.cleaned_data['artist3'],
                    vibe=form.cleaned_data['vibe'],
                    date_of_inquiry = timezone.now()
                )
                inquiry.save()

                # Create Song instances using form data
                for i in range(15):
                    song = Song(
                        song_title = song_titles[i],
                        artist_name = artist_names[i],
                        inquiry = inquiry
                    )
                    song.save()

                # Redirect to a success page or another view
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