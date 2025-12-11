"""
Views for the CardioGuard Assistant application.
"""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def home(request):
    """Render the home landing page."""
    return render(request, 'home.html')


def auth(request):
    """Render the authentication page (sign in / sign up)."""
    return render(request, 'auth.html')


@csrf_exempt
@require_http_methods(["POST"])
def predict(request):
    """
    API endpoint for heart disease risk prediction.
    
    Expects JSON body with:
        - age: Patient age (years)
        - gender: 0 = Female, 1 = Male
        - heart_rate: Heart rate (bpm)
        - systolic_bp: Systolic blood pressure (mmHg)
        - diastolic_bp: Diastolic blood pressure (mmHg)
        - blood_sugar: Blood sugar level (mg/dL)
        - ck_mb: CK-MB enzyme level
        - troponin: Troponin level
    
    Returns JSON with prediction results.
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'heart_rate', 'systolic_bp',
            'diastolic_bp', 'blood_sugar', 'ck_mb', 'troponin'
        ]
        
        missing = [f for f in required_fields if f not in data]
        if missing:
            return JsonResponse({
                'error': f'Missing required fields: {", ".join(missing)}'
            }, status=400)
        
        # Convert to proper types
        patient_data = {
            'age': float(data['age']),
            'gender': int(data['gender']),
            'heart_rate': float(data['heart_rate']),
            'systolic_bp': float(data['systolic_bp']),
            'diastolic_bp': float(data['diastolic_bp']),
            'blood_sugar': float(data['blood_sugar']),
            'ck_mb': float(data['ck_mb']),
            'troponin': float(data['troponin'])
        }
        
        # Get prediction
        from .ml_model import predict_risk
        result = predict_risk(patient_data)
        
        return JsonResponse({
            'success': True,
            'prediction': result
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON in request body'
        }, status=400)
    except FileNotFoundError as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
    except (ValueError, TypeError) as e:
        return JsonResponse({
            'error': f'Invalid data format: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Prediction failed: {str(e)}'
        }, status=500)
