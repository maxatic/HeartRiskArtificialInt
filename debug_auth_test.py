import requests

BASE_URL = 'http://127.0.0.1:8000'
EMAIL = 'debug_doctor_shell' # Username is the email/name used in shell
PASSWORD = 'testpass'

def test_login():
    print(f"\n--- Testing Login for {EMAIL} as Doctor ---")
    url = f"{BASE_URL}/api/login/"
    data = {
        'username': EMAIL,
        'password': PASSWORD,
        'role': 'doctor'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login Response Code: {response.status_code}")
        if response.status_code == 200:
             print("Login Success!")
        else:
             print(f"Login Failed: {response.text}")
             
    except Exception as e:
         print(f"Login Request Failed: {e}")

if __name__ == "__main__":
    test_login()
