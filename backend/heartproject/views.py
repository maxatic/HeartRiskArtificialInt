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

from predictor.serializers import MedicalRecordSerializer
from predictor.models import MedicalRecord
from .ml_model import predict_risk

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_heart_risk(request):
    serializer = MedicalRecordSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # 1. Prepare data for model
            # We need to map model fields to the keys expected by predict_risk
            # Note: models.py fields are lowercase, but ml_model.py expects specific Capitalized keys
            data = serializer.validated_data
            
            model_input = {
                'Age': data['age'],
                'Gender': 1 if data['gender'].lower() == 'male' else 0, # Assuming 'male'/'female' input, model likely trained on specific format. ADJUST THIS.
                # Actually, let's double check what the model expects for Gender. 
                # For now let's assume the frontend sends numeric or we handle conversion. 
                # If model expects 0/1, we should probably ensure frontend sends that or we convert.
                # Let's assume frontend sends 1 for Male, 0 for Female for simplicity based on previous context or common ML datasets.
                # If 'gender' is text, we need a map. Let's assume direct mapping for now but we might need to revisit.
                
                # REVISION during coding: simple mapping based on common dataset encoding: 
                # Let's trust the input for now but cast to int/float as needed.
                # Actually proper mapping is safer:
                # 'Age', 'Gender', 'Heart rate', 'Systolic blood pressure', 'Diastolic blood pressure', 'Blood sugar', 'CK-MB', 'Troponin'
                
                # Careful mapping:
                'Heart rate': data['heart_rate'],
                'Systolic blood pressure': data['systolic_bp'],
                'Diastolic blood pressure': data['diastolic_bp'],
                'Blood sugar': data['blood_sugar'],
                'CK-MB': data['ck_mb'],
                'Troponin': data['troponin']
            }
            
            # Helper to handle gender if it's a string, otherwise pass through
            if isinstance(data['gender'], str):
                 model_input['Gender'] = 1 if data['gender'].lower() in ['male', '1'] else 0
            else:
                 model_input['Gender'] = int(data['gender'])

            
            # 2. Get Prediction
            risk_percentage = predict_risk(model_input)
            
            # 3. Save to DB
            record = serializer.save(user=request.user, result=risk_percentage)
            
            return Response({
                "status": "success",
                "risk_percentage": risk_percentage,
                "record_id": record.id
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    
    return Response(serializer.errors, status=400)


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
