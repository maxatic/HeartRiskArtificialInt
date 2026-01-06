from rest_framework import serializers
from .models import MedicalRecord

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
