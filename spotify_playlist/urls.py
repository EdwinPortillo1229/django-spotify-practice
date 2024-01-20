from django.urls import path
from .views import create_inquiry, inquiries_index, inquiry_detail, connect_to_spotify, spotify_set_user

urlpatterns = [
    path('create_inquiry/<int:user_pk>/', create_inquiry, name='create_inquiry'),
    path('inquiries_index/<int:user_pk>/', inquiries_index, name='inquiries_index'),
    path('inquiry_detail/<int:pk>/', inquiry_detail, name='inquiry_detail'),
    path('connect_to_spotify/', connect_to_spotify, name='connect_to_spotify'),
    path('spotify_set_user/', spotify_set_user, name='spotify_set_user')
]
