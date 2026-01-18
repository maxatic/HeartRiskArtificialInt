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
    path('api/user-profile/', views.get_user_profile, name='get_user_profile'),
    path('api/predict-risk/', views.predict_heart_risk, name='predict_risk'),
    path('predict/', views.predict_page, name='predict_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
]
