from django.http import HttpResponse


def landing_page(request):
    return HttpResponse("Hello, world. You're at the landing page!")