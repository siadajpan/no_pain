import requests
import sys

BASE_URL = "http://localhost:8001"

def register_user(email, password, role, first_name=None, last_name=None, street_address=None, city=None, postcode=None, practice_name=None, phone=None):
    url = f"{BASE_URL}/register/"
    data = {
        "email": email,
        "password": password,
        "repeat_password": password,
        "role": role,
        "tos_agreement": "true",
        "street_address": street_address,
        "city": city,
        "postcode": postcode,
        "first_name": first_name,
        "last_name": last_name,
        "practice_name": practice_name,
        "phone": phone
    }
    print(f"Registering {role}: {email}...")
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 and "Confirm your email" in response.text:
            print(f"SUCCESS: {role} registered.")
            return True
        else:
            print(f"FAILED: {role} registration. Status: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def verify_db(email, role):
    # This part would ideally query the DB directly, but for now we trust the registration response
    # and maybe try to login or check if we can inspect via a side channel if needed.
    # For this script, success response is good enough for step 1.
    pass

if __name__ == "__main__":
    success = True
    success &= register_user("patient@example.com", "password", "patient", first_name="Pat", last_name="Patient")
    success &= register_user("doctor@example.com", "password", "doctor", first_name="Doc", last_name="Doctor")
    success &= register_user("practice@example.com", "password", "practice", practice_name="City Dental", street_address="123 Main St", city="London", postcode="EC1A 1BB", phone="555-1234")

    if not success:
        sys.exit(1)
    print("All roles registered successfully.")
