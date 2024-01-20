# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryForm
from .models import Inquiry
from django.utils import timezone

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
    return render(request, 'spotify_playlist/inquiry_detail.html', {'inquiry': inquiry})