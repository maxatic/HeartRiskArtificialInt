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
    path('api/predict-risk/', views.predict_heart_risk, name='predict_risk'),
    path('api/history/', views.get_patient_history, name='get_patient_history'),
    path('predict/', views.predict_page, name='predict_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]
