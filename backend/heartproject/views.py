"""
For coding this part of the backend we used Antigravity with Gemini 3.1 Pro
"""
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    full_name = user.get_full_name().strip()
    
    # Determine role
    # If this user is in the Doctor group or has added patients, they are a doctor
    is_doctor = user.groups.filter(name='Doctor').exists() or Patient.objects.filter(doctor=user).exists()
    role = 'doctor' if is_doctor else 'patient'

    return Response({
        "full_name": full_name,
        #these 3 we need because of Django's built-in User model
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,

        "email": user.email,
        "role": role
    })

from predictor.serializers import MedicalRecordSerializer, PatientSerializer
from predictor.models import MedicalRecord, Patient
from .ml_model import predict_risk

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_heart_risk(request):
    # Determine target user
    # If a patient_id is provided in the request, 
    # it assumes a Doctor is making the prediction for one of their patients (and verifies they have permission). 
    # Otherwise, it assumes the logged-in user is a patient doing a self-assessment.
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
            # Prepare data for model
            # We need to map model fields to the keys expected by predict_risk
            data = serializer.validated_data
            # It maps the data from the serializer to the model_input dictionary
            model_input = {
                'Age': data['age'],
                # Gender is 1 for male, 0 for female
                # As we have only 2 options (drop-down menu on frontend), we can use a simple if-else statement
                'Gender': 1 if data['gender'].lower() == 'male' else 0, 
                'Heart rate': data['heart_rate'],
                'Systolic blood pressure': data['systolic_bp'],
                'Diastolic blood pressure': data['diastolic_bp'],
                'Blood sugar': data['blood_sugar'],

                'CK-MB': data.get('ck_mb') if data.get('ck_mb') is not None else None,
                'Troponin': data.get('troponin') if data.get('troponin') is not None else None
            }

            # Get Prediction and Explanations
            # Check if we should use the reduced model
            # Logic: If CK-MB and Troponin are explicitly missing (None/empty string), use 6-feature model. 
            # Explicit 0s are valid.
            use_reduced = False
            ck_mb_val = data.get('ck_mb')
            trop_val = data.get('troponin')
            
            # Differentiating between an explicit 0 test result and a missing test result
            if (ck_mb_val is None or ck_mb_val == "") and (trop_val is None or trop_val == ""):
                use_reduced = True
            else:
                # If they provided only one, or they provided 0s, ensure they have a numeric fallback for the full model
                model_input['CK-MB'] = ck_mb_val if ck_mb_val is not None and ck_mb_val != "" else 0
                model_input['Troponin'] = trop_val if trop_val is not None and trop_val != "" else 0
                
            risk_percentage, shap_values = predict_risk(model_input, use_reduced_model=use_reduced)
            
            # Save to DB
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

# Fetch recent assessments for the logged-in user.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_history(request):
    records = MedicalRecord.objects.filter(user=request.user).order_by('-created_at')[:10] # Get last 10
    serializer = MedicalRecordSerializer(records, many=True)
    return Response(serializer.data)


# Fetch a specific assessment details and history.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_assessment_detail(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    #The following code is written by Antigravity with Gemini 3.1 Pro
    #It's a security check to make sure that the user has permission to view the record called nsecure Direct Object Reference (IDOR).
    #If we don't have this check, any user can view any record by changing the URL.
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

    # Get Patient ID if doctor
    patient_id = None
    if viewer_role == 'doctor':
        try:
            p = Patient.objects.get(user=record.user, doctor=request.user)
            patient_id = p.id
        except Patient.DoesNotExist:
            pass

    # Check if the current user is a doctor (generic check)
    is_doctor_user = False
    if request.user.groups.filter(name='Doctor').exists() or Patient.objects.filter(doctor=request.user).exists():
        is_doctor_user = True

    return Response({
        "record": serializer.data,
        "history": history_data,
        "viewer_role": viewer_role,
        "patient_name": patient_name.strip(),
        "is_partial_assessment": is_partial,
        "patient_id": patient_id,
        "is_doctor_user": is_doctor_user
    })


def home(request):
    #Render the home landing page.
    return render(request, 'home.html')

def predict_page(request):
    #Render the prediction interface.
    return render(request, 'predict.html')


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

def auth(request):
    #Render the authentication page (sign in / sign up).
    if request.method == 'POST' and request.POST.get('form_type') == 'signup':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name', '').strip()
        
        #Simple validation, if the user with this email already exists
        #It makes the email unique.
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
            # The following code is written by Antigravity with Gemini 3.1 Pro
            # It assigns the user to a role group (doctor or patient).  
            role = request.POST.get('role')
            if role in ['doctor', 'patient']:
                from django.contrib.auth.models import Group
                group, created = Group.objects.get_or_create(name=role.capitalize()) # 'Doctor' or 'Patient'
                user.groups.add(group)
                
                # Check for Doctor Email if role is Patient
                if role == 'patient':
                    doctor_email = request.POST.get('doctor_email', '').strip()
                    if doctor_email:
                        try:
                            doctor_user = User.objects.get(email=doctor_email)
                            # Verify this user is actually a doctor (optional but good practice)
                            if doctor_user.groups.filter(name='Doctor').exists() or Patient.objects.filter(doctor=doctor_user).exists():
                                from predictor.models import Patient
                                Patient.objects.create(
                                    doctor=doctor_user,
                                    user=user
                                )
                        except User.DoesNotExist:
                            # If doctor email is not found, rollback user creation and show error.
                            user.delete() # Rollback
                            messages.error(request, f'Doctor with email "{doctor_email}" not found. Please check the email or leave blank.')
                            return render(request, 'auth.html')

            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('auth')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            
    return render(request, 'auth.html')

# Checks if username and password match the database
from django.contrib.auth import authenticate
# Generates the secure digital ID badge (JWT) for logged-in users
from rest_framework_simplejwt.tokens import RefreshToken
# Allows applying security rules like locks to specific API endpoints
from rest_framework.decorators import permission_classes
# A specific security rule that leaves the endpoint unlocked for anyone
from rest_framework.permissions import AllowAny

# Handles login requests including role validation
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role') # 'doctor' or 'patient'
    
    if not username or not password:
         return Response({'error': 'Please provide both username and password'}, status=400)
         
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if role:
            # Check if user belongs to the requested role group
            group_name = role.capitalize()
            
            if not user.groups.filter(name=group_name).exists():
                return Response({'error': f'Access denied: You are not registered as a {role}.'}, status=403)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

# Handles rendering the patient dashboard
def dashboard(request):
    return render(request, 'dashboard.html')

# Handles rendering the doctor dashboard
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

# Render the detailed result page. Data fetched via JS.
def result_page(request, record_id):
    return render(request, 'result.html', {'record_id': record_id})

#API to add a new patient for the logged-in doctor by email.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient(request):
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

#API to get list of patients for the logged-in doctor.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_patients(request):
    patients = Patient.objects.filter(doctor=request.user).order_by('-created_at')
    # Part where we calculate the tisk for each patient and add it to the response.
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
            # We decided to use 70 as the threshold for high risk and measure the average for the last 5 records.
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

"""
    API for DOCTORS to view the history of a specific patient they have added.
    patient_id is the ID of the  record in the Patient table (not the User ID).
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_specific_patient_history(request, patient_id):
    # The following code is written by Antigravity with Gemini 3.1 Pro
    # This acts as a security check (Data Protection).
    # It ensures that doctors can only view the history of patients they have explicitly added.
    # If a doctor tries to View/Predict using another doctor's patient_id, it blocks them with a 404 error.
    patient_record = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    target_user = patient_record.user
    
    records = MedicalRecord.objects.filter(user=target_user).order_by('-created_at')
    history_serializer = MedicalRecordSerializer(records, many=True)
    patient_serializer = PatientSerializer(patient_record)
    
    return Response({
        "patient": patient_serializer.data,
        "history": history_serializer.data
    })
# Render the detailed patient history dashboard.
# We pass the patient_id to the template so it can fetch data via JS
def patient_history_dashboard(request, patient_id):
    return render(request, 'doctor dashboard 2.html', {'patient_id': patient_id})
