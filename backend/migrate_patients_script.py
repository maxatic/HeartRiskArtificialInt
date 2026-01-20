
import os
import django
import sys
import random
import string

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heartproject.settings')
django.setup()

from django.contrib.auth.models import User
from predictor.models import Patient

def generate_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def migrate_patients():
    patients = Patient.objects.filter(user__isnull=True)
    print(f"Found {patients.count()} patients to migrate.")
    
    migrated_count = 0
    created_users = 0

    for patient in patients:
        email = patient.email
        if not email:
            print(f"Skipping patient {patient.id}: No email found.")
            # For testing/dev, maybe generate a fake one? 
            # Let's skip for now or generate based on ID if critical.
            # Generated:
            email = f"patient_{patient.id}@example.com"
            print(f"Generated email for patient {patient.id}: {email}")

        # Check if user exists
        user = User.objects.filter(email=email).first()
        
        if not user:
            # Create new user
            username = email
            # Handle username collision just in case (though email matched check failed)
            if User.objects.filter(username=username).exists():
                username = f"{email}_{patient.id}"
            
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=generate_password(),
                    first_name=patient.first_name or "",
                    last_name=patient.last_name or ""
                )
                created_users += 1
                print(f"Created User for {email}")
            except Exception as e:
                print(f"Error creating user for {email}: {e}")
                continue
        else:
            print(f"Found existing User for {email}")

        # Link patient
        patient.user = user
        patient.save()
        migrated_count += 1
    
    print(f"Migration Complete. Linked {migrated_count} patients. Created {created_users} new users.")

if __name__ == "__main__":
    migrate_patients()
