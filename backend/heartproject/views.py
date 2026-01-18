"""
Views for the CardioGuard Assistant application.
"""
from django.shortcuts import render, get_object_or_404
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    full_name = user.get_full_name().strip()
    return Response({
        "full_name": full_name,
        "username": user.username,
        "email": user.email,
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

            
            
            # 2. Get Prediction and Explanations
            risk_percentage, shap_values = predict_risk(model_input)
            
            # 3. Save to DB
            record = serializer.save(
                user=request.user, 
                result=risk_percentage,
                shap_values=shap_values
            )
            
            return Response({
                "status": "success",
                "risk_percentage": risk_percentage,
                "shap_values": shap_values, 
                "record_id": record.id
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_history(request):
    """Fetch recent assessments for the logged-in user."""
    records = MedicalRecord.objects.filter(user=request.user).order_by('-created_at')[:10] # Get last 10
    serializer = MedicalRecordSerializer(records, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assessment_detail(request, record_id):
    """
    API endpoint to fetch a specific assessment details and history.
    """
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)
    serializer = MedicalRecordSerializer(record)
    
    # Get history for trend chart
    history_qs = MedicalRecord.objects.filter(user=request.user).order_by('created_at')
    history_data = []
    for h in history_qs:
        history_data.append({
            'id': h.id,
            'date': h.created_at.strftime('%d/%m'),
            'score': h.result
        })
        
    return Response({
        "record": serializer.data,
        "history": history_data
    })


def home(request):
    """Render the home landing page."""
    return render(request, 'home.html')

def predict_page(request):
    """Render the prediction interface."""
    return render(request, 'predict.html')


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

def auth(request):
    """Render the authentication page (sign in / sign up)."""
    if request.method == 'POST' and request.POST.get('form_type') == 'signup':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name', '').strip()
        
        # Simple validation
        if User.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
            return render(request, 'auth.html')

        # Create user (using email as username)
        try:
            user = User.objects.create_user(username=email, email=email, password=password) #Django's default User model requires a username. It's a mandatory field in the database.
            if full_name:
                name_parts = full_name.split()
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = " ".join(name_parts[1:])
            user.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('auth')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            
    return render(request, 'auth.html')

def dashboard(request):
    """Render the patient dashboard."""
    return render(request, 'dashboard.html')

def doctor_dashboard(request):
    """Render the doctor dashboard."""
    return render(request, 'doctor_dashboard.html')

def result_page(request, record_id):
    """Render the detailed result page. Data fetched via JS."""
    return render(request, 'result.html', {'record_id': record_id})

