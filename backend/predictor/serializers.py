from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = [
            'age', 'gender', 'heart_rate', 
            'systolic_bp', 'diastolic_bp', 
            'blood_sugar', 'ck_mb', 'troponin'
        ]
