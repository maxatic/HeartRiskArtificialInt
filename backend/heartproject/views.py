"""
Views for the CardioGuard Assistant application.
"""
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_health_summary(request):
    # 'request.user' is automatically identified by the JWT Token
    return Response({
        "status": "Secure Access Granted",
    })

def home(request):
    """Render the home landing page."""
    return render(request, 'home.html')


def auth(request):
    """Render the authentication page (sign in / sign up)."""
    return render(request, 'auth.html')
