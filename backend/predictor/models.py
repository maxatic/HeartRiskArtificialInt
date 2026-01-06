from django.db import models
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    # Link record to a user (optional, if you want to track who the record belongs to)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    age = models.IntegerField()
    gender = models.CharField(max_length=10) # Using CharField to be flexible (e.g., "Male", "Female", or '0'/'1')
    heart_rate = models.IntegerField()
    systolic_bp = models.IntegerField(verbose_name="Systolic blood pressure")
    diastolic_bp = models.IntegerField(verbose_name="Diastolic blood pressure")
    blood_sugar = models.FloatField()
    ck_mb = models.FloatField(verbose_name="CK-MB")
    troponin = models.FloatField()

    # Store the prediction result (risk percentage)
    result = models.FloatField(blank=True, null=True, help_text="Risk percentage (0-100)")
    
    # Store SHAP values for explainability
    shap_values = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.id} - {self.result}"
