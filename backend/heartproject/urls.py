"""
URL configuration for heartproject.
"""
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView, # Sends refresh token here to get new access token
)

urlpatterns = [
    #HTML PAGE ROUTES
    path('', views.home, name='home'), # Landing page
    path('auth/', views.auth, name='auth'), # Sign Up / Sign In page
    path('predict/', views.predict_page, name='predict_page'), # Patient risk assessment form page
    path('result/<int:record_id>/', views.result_page, name='result_page'), # Prediction visual results page
    path('dashboard/', views.dashboard, name='dashboard'), # Patient's personal history dashboard
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'), # Doctor's main patient list dashboard
    path('doctor/patient/<int:patient_id>/', views.patient_history_dashboard, name='patient_history_dashboard'), # Doctor's detailed view of a specific patient's history

    # API endpoints
    # Authentication & Tokens
    path('api/login/', views.api_login, name='api_login'), # Returns Access and Refresh tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Sends refresh token here to get new access token
    
    # Core User Actions
    path('api/me/', views.get_profile, name='get_profile'), # Fetches logged-in user's profile info (name, role)
    path('api/predict-risk/', views.predict_heart_risk, name='predict_risk'), # Submit form data to ML model to calculate risk
    
    # Patient Data Retrieval
    path('api/history/', views.get_patient_history, name='get_patient_history'), # Fetch the last 10 records for logged-in patient
    path('api/result/<int:record_id>/', views.get_assessment_detail, name='get_assessment_detail'), # Fetch full details of one specific record
    
    # Doctor Specific Features
    path('api/patients/add/', views.add_patient, name='add_patient'), # Doctor adds a patient using their email
    path('api/patients/', views.get_doctor_patients, name='get_doctor_patients'), # Doctor fetches list of their active patients with risk summaries
    path('api/patients/<int:patient_id>/history/', views.get_specific_patient_history, name='get_specific_patient_history'), # Doctor fetches full history of one specific linked patient
]
