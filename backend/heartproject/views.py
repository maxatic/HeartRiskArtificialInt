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


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

def auth(request):
    """Render the authentication page (sign in / sign up)."""
    if request.method == 'POST' and request.POST.get('form_type') == 'signup':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Simple validation
        if User.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
            return render(request, 'auth.html')

        # Create user (using email as username)
        try:
            user = User.objects.create_user(username=email, email=email, password=password) #Django's default User model requires a username. It's a mandatory field in the database.
            user.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('auth')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            
    return render(request, 'auth.html')
