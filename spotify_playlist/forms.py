# spotify_playlist/forms.py

from django import forms

class InquiryForm(forms.Form):
    artist1 = forms.CharField(max_length=255)
    artist2 = forms.CharField(max_length=255)
    artist3 = forms.CharField(max_length=255)
