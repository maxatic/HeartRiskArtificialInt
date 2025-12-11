"""
Views for the CardioGuard Assistant application.
"""
from django.shortcuts import render


def home(request):
    """Render the home landing page."""
    return render(request, 'home.html')


def auth(request):
    """Render the authentication page (sign in / sign up)."""
    return render(request, 'auth.html')
