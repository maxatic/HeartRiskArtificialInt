import os
import sys
import django
import json

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heartproject.settings')
django.setup()

from predictor.models import MedicalRecord, Patient
from django.forms.models import model_to_dict

def dump_model(model_class, limit=5):
    print(f"--- Data for {model_class.__name__} (First {limit} rows) ---")
    objects = model_class.objects.all()[:limit]
    if not objects:
        print("No records found.")
    for obj in objects:
        data = model_to_dict(obj)
        # Handle datetime serialization if necessary (model_to_dict might pass them as objects)
        print(data)
    print("\n")

if __name__ == "__main__":
    print("Dumping database content...\n")
    dump_model(MedicalRecord)
    dump_model(Patient)
