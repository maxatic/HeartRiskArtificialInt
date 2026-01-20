from rest_framework import serializers
from .models import MedicalRecord, Patient

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'age', 'gender', 'heart_rate', 
            'systolic_bp', 'diastolic_bp', 
            'blood_sugar', 'ck_mb', 'troponin',
            'result', 'created_at', 'shap_values'
        ]
        read_only_fields = ['id', 'result', 'created_at', 'shap_values']

class PatientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'doctor', 'user', 'first_name', 'last_name', 'email', 'patient_id', 'age', 'created_at']
        read_only_fields = ['doctor', 'created_at', 'user']
