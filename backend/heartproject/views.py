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
    
    # Determine role
    # If this user has added patients, they are a doctor
    is_doctor = Patient.objects.filter(doctor=user).exists()
    role = 'doctor' if is_doctor else 'patient'

    return Response({
        "full_name": full_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "role": role
    })

from predictor.serializers import MedicalRecordSerializer
from predictor.serializers import MedicalRecordSerializer, PatientSerializer
from predictor.models import MedicalRecord, Patient
from .ml_model import predict_risk

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_heart_risk(request):
    # Determine target user
    target_user = request.user
    patient_id = request.data.get('patient_id')
    
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id, doctor=request.user)
            target_user = patient.user
        except Patient.DoesNotExist:
            return Response({"error": "Invalid patient ID or permission denied"}, status=403)
            
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
                'CK-MB': data.get('ck_mb', 0) or 0,
                'Troponin': data.get('troponin', 0) or 0
            }
            
            # Helper to handle gender if it's a string, otherwise pass through
            if isinstance(data['gender'], str):
                 model_input['Gender'] = 1 if data['gender'].lower() in ['male', '1'] else 0
            else:
                 model_input['Gender'] = int(data['gender'])

            
            
            # 2. Get Prediction and Explanations
            
            # Check if we should use the reduced model
            # Logic: If CK-MB and Troponin are effectively 0 (not provided), use 6-feature model
            use_reduced = False
            ck_mb_val = data.get('ck_mb', 0)
            trop_val = data.get('troponin', 0)
            
            if (ck_mb_val == 0 or ck_mb_val is None) and (trop_val == 0 or trop_val is None):
                use_reduced = True
                
            risk_percentage, shap_values = predict_risk(model_input, use_reduced_model=use_reduced)
            
            # 3. Save to DB
            record = serializer.save(
                user=target_user, 
                result=risk_percentage,
                shap_values=shap_values
            )
            
            return Response({
                "status": "success",
                "risk_percentage": risk_percentage,
                "shap_values": shap_values, 
                "record_id": record.id,
                "is_partial_assessment": use_reduced
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
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    # Check permissions: User owns record OR User is doctor of the record owner
    has_permission = False
    if record.user == request.user:
        has_permission = True
    elif Patient.objects.filter(doctor=request.user, user=record.user).exists():
        has_permission = True
        
    if not has_permission:
        return Response({"error": "Permission denied"}, status=403)

    # Fetch history for chart (all records for this user)
    history = MedicalRecord.objects.filter(user=record.user).order_by('created_at')
    
    # Serialize
    serializer = MedicalRecordSerializer(record)
    
    # Simple history data for chart
    history_data = []
    for h in history:
        history_data.append({
            'id': h.id,
            'date': h.created_at.strftime("%Y-%m-%d"),
            'score': h.result
        })
        
    # Determine viewer role and patient name
    viewer_role = 'patient'
    patient_name = record.user.get_full_name() or record.user.email
    
    if record.user != request.user:
        # If the viewer is not the owner, they must be the doctor (checked above)
        viewer_role = 'doctor'

    # Determine if this was a partial assessment
    # Check if CK-MB and Troponin are 0
    is_partial = False
    if record.ck_mb == 0 and record.troponin == 0:
        is_partial = True

    return Response({
        "record": serializer.data,
        "history": history_data,
        "viewer_role": viewer_role,
        "patient_name": patient_name.strip(),
        "is_partial_assessment": is_partial
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

        # Create user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            if full_name:
                name_parts = full_name.split()
                user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = " ".join(name_parts[1:])
            user.save()
            
            # Assign Role Group
            role = request.POST.get('role')
            print(f"DEBUG SIGNUP: Received role '{role}'")
            if role in ['doctor', 'patient']:
                from django.contrib.auth.models import Group
                group, created = Group.objects.get_or_create(name=role.capitalize()) # 'Doctor' or 'Patient'
                print(f"DEBUG SIGNUP: Group '{group.name}' (Created: {created})")
                user.groups.add(group)
                print(f"DEBUG SIGNUP: Added user {user.username} to group {group.name}")

            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('auth')
        except Exception as e:
            print(f"DEBUG SIGNUP ERROR: {str(e)}")
            messages.error(request, f'Error creating account: {str(e)}')
            
    return render(request, 'auth.html')

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Custom login view to enforce role checks.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role') # 'doctor' or 'patient'
    
    print(f"DEBUG LOGIN: Attempting login for '{username}' as '{role}'")
    
    if not username or not password:
         return Response({'error': 'Please provide both username and password'}, status=400)
         
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if role:
            # Check if user belongs to the requested role group
            # We assume group names are 'Doctor' and 'Patient'
            group_name = role.capitalize()
            user_groups = list(user.groups.values_list('name', flat=True))
            print(f"DEBUG LOGIN: User groups: {user_groups}. Required: {group_name}")
            
            if not user.groups.filter(name=group_name).exists():
                print(f"DEBUG LOGIN: Role mismatch!")
                return Response({'error': f'Access denied: You are not registered as a {role}.'}, status=403)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


def dashboard(request):
    """Render the patient dashboard."""
    return render(request, 'dashboard.html')

def doctor_dashboard(request):
    """Render the doctor dashboard."""
    return render(request, 'doctor_dashboard.html')

def result_page(request, record_id):
    """Render the detailed result page. Data fetched via JS."""
    return render(request, 'result.html', {'record_id': record_id})

    return render(request, 'result.html', {'record_id': record_id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient(request):
    """API to add a new patient for the logged-in doctor by email."""
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=400)
    
    # Find user by email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User with this email not found. Please ask patient to sign up first."}, status=404)
    
    # Check if already added
    if Patient.objects.filter(doctor=request.user, user=user).exists():
         return Response({"error": "Patient already added"}, status=400)

    # Create link
    # We can optionally accept age/patient_id if sent, but mainly just email is used now.
    patient = Patient.objects.create(
        doctor=request.user,
        user=user,
        patient_id=request.data.get('patient_id'),
        age=request.data.get('age')
    )
    
    serializer = PatientSerializer(patient)
    return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_patients(request):
    """API to get list of patients for the logged-in doctor."""
    patients = Patient.objects.filter(doctor=request.user).order_by('-created_at')
    
    # Calculate risk stats for each patient
    patient_data = []
    for patient in patients:
        # Get patient serializer data
        p_data = PatientSerializer(patient).data
        
        # Fetch last 5 records
        records = MedicalRecord.objects.filter(user=patient.user).order_by('-created_at')[:5]
        
        if records.exists():
            latest_score = records[0].result or 0
            
            # Calculate average of last 5
            # Filter out None results just in case
            valid_scores = [r.result for r in records if r.result is not None]
            avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            
            # Determine Risk Status
            # Logic: High Risk if (Avg > 70) OR (Latest > 70)
            if latest_score > 70 or avg_score > 70:
                risk_status = 'High'
            elif avg_score > 30:
                risk_status = 'Moderate'
            else:
                risk_status = 'Low'
                
            p_data['risk_status'] = risk_status
            p_data['latest_score'] = round(latest_score, 1)
            p_data['average_score'] = round(avg_score, 1)
        else:
            p_data['risk_status'] = 'Unknown'
            p_data['latest_score'] = 0
            p_data['average_score'] = 0
            
        patient_data.append(p_data)
        
    return Response(patient_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_specific_patient_history(request, patient_id):
    """
    API for DOCTORS to view the history of a specific patient they have added.
    patient_id is the ID of the Patient record (not the User ID).
    """
    # Verify the patient belongs to this doctor
    patient_record = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    target_user = patient_record.user
    
    records = MedicalRecord.objects.filter(user=target_user).order_by('-created_at')
    history_serializer = MedicalRecordSerializer(records, many=True)
    patient_serializer = PatientSerializer(patient_record)
    
    return Response({
        "patient": patient_serializer.data,
        "history": history_serializer.data
    })

def patient_history_dashboard(request, patient_id):
    """Render the detailed patient history dashboard."""
    # We pass the patient_id to the template so it can fetch data via JS
    return render(request, 'doctor dashboard 2.html', {'patient_id': patient_id})
