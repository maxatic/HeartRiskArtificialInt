"""
URL configuration for heartproject.
"""
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView, #generating access and refresh tokens
    TokenRefreshView, #refreshing access token
)

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth, name='auth'),
    # endpoint, where 'Login' - returns Access and Refresh tokens
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # endpoint, where 'Renewer' - send refresh token here to get new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', views.get_profile, name='get_profile'),
    path('api/predict-risk/', views.predict_heart_risk, name='predict_risk'),
    path('api/history/', views.get_patient_history, name='get_patient_history'),
    path('api/result/<int:record_id>/', views.get_assessment_detail, name='get_assessment_detail'),
    path('predict/', views.predict_page, name='predict_page'),
    path('result/<int:record_id>/', views.result_page, name='result_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('api/patients/add/', views.add_patient, name='add_patient'),
    path('api/patients/', views.get_doctor_patients, name='get_doctor_patients'),
    path('api/patients/<int:patient_id>/history/', views.get_specific_patient_history, name='get_specific_patient_history'),
    path('doctor/patient/<int:patient_id>/', views.patient_history_dashboard, name='patient_history_dashboard'),
    
]
