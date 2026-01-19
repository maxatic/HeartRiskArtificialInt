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
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['doctor', 'created_at']
