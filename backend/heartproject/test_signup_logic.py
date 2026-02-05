from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from predictor.models import Patient

class SignupDoctorLinkTest(TestCase):
    def setUp(self):
        # Create groups
        self.doctor_group = Group.objects.create(name='Doctor')
        self.patient_group = Group.objects.create(name='Patient')
        
        # Create a doctor
        self.doctor_user = User.objects.create_user(username='doc@test.com', email='doc@test.com', password='password')
        self.doctor_user.groups.add(self.doctor_group)
        self.doctor_user.save()
        
        self.client = Client()
        self.signup_url = '/auth/' # Assuming this is the URL for auth view based on views.py

    def test_signup_with_valid_doctor_email(self):
        response = self.client.post(self.signup_url, {
            'form_type': 'signup',
            'email': 'patient@test.com',
            'password': 'password',
            'confirm_password': 'password', # Current view doesn't seem to check confirm_password but good to have
            'full_name': 'Test Patient',
            'role': 'patient',
            'doctor_email': 'doc@test.com'
        })
        
        # Check if patient user created
        self.assertTrue(User.objects.filter(email='patient@test.com').exists())
        patient_user = User.objects.get(email='patient@test.com')
        
        # Check if linked to doctor
        self.assertTrue(Patient.objects.filter(user=patient_user, doctor=self.doctor_user).exists())
        
    def test_signup_with_invalid_doctor_email(self):
        response = self.client.post(self.signup_url, {
            'form_type': 'signup',
            'email': 'patient_fail@test.com',
            'password': 'password',
            'full_name': 'Test Patient Fail',
            'role': 'patient',
            'doctor_email': 'fake@test.com'
        })
        
        # Check that user was NOT created (rollback logic)
        self.assertFalse(User.objects.filter(email='patient_fail@test.com').exists())
        
    def test_signup_without_doctor_email(self):
        response = self.client.post(self.signup_url, {
            'form_type': 'signup',
            'email': 'patient_independent@test.com',
            'password': 'password',
            'full_name': 'Test Patient Indep',
            'role': 'patient',
            'doctor_email': ''
        })
        
        # Check if patient user created
        self.assertTrue(User.objects.filter(email='patient_independent@test.com').exists())
        patient_user = User.objects.get(email='patient_independent@test.com')
        
        # Check valid user but NO patient record linked to any doctor (or at least not this one)
        # Note: Logic only creates Patient record if linked to doctor currently?
        # Let's check views.py again. 
        # Logic: 
        # if role == 'patient':
        #    ... if doctor_email: ... Patient.objects.create(...)
        # So if no doctor email, no Patient record is created? 
        # That might be existing behavior or a gap, but for this task I am testing my changes.
        
        self.assertFalse(Patient.objects.filter(user=patient_user).exists())
