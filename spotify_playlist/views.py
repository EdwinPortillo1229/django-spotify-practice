from django.shortcuts import render, redirect
from .forms import InquiryForm

def create_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Process the form data (save to the database, etc.)
            # Redirect to a success page or another view
            return redirect('success_page')
    else:
        form = InquiryForm()

    return render(request, 'spotify_playlist/create_inquiry.html', {'form': form})
