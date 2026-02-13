import requests

BASE_URL = "http://localhost:8001"

def login(email, password):
    session = requests.Session()
    login_url = f"{BASE_URL}/login"
    response = session.post(login_url, data={"email": email, "password": password})
    if response.url.rstrip("/") == f"{BASE_URL}":
        return session
    return None

def verify_patient_dashboard():
    print("--- Verifying Patient Dashboard ---")
    session = login("patient@example.com", "password")
    if not session:
        print("FAILED: Could not login as patient.")
        return False
    response = session.get(f"{BASE_URL}/")
    if "Registered Doctors" in response.text and "Registered Practices" in response.text:
        print("SUCCESS: Patient dashboard loaded correctly.")
        return True
    else:
        print("FAILED: Patient dashboard missing key elements.")
        return False

def verify_doctor_dashboard():
    print("--- Verifying Doctor Dashboard ---")
    session = login("doctor@example.com", "password")
    if not session:
        print("FAILED: Could not login as doctor.")
        return False
    response = session.get(f"{BASE_URL}/")
    if "My Practices" in response.text and "Join a Practice" in response.text:
        print("SUCCESS: Doctor dashboard loaded correctly.")
        return True
    else:
        print("FAILED: Doctor dashboard content mismatch.")
        return False

def verify_practice_dashboard():
    print("--- Verifying Practice Dashboard ---")
    session = login("practice@example.com", "password")
    if not session:
        print("FAILED: Could not login as practice.")
        return False
    response = session.get(f"{BASE_URL}/")
    if "My Doctors" in response.text and "Add a Doctor" in response.text:
        print("SUCCESS: Practice dashboard loaded correctly.")
        return True
    else:
        print("FAILED: Practice dashboard content mismatch.")
        return False

def verify_practice_add_doctor():
    print("--- Verifying Practice Add Doctor API ---")
    session = login("practice@example.com", "password")
    if not session:
        print("FAILED: Could not login as practice.")
        return False
    # Search doctors
    response = session.get(f"{BASE_URL}/api/doctors/search?q=")
    if response.status_code == 200:
        doctors = response.json()
        print(f"  Found {len(doctors)} doctors in search.")
        if len(doctors) > 0:
            doctor_id = doctors[0]["id"]
            # Add doctor
            response = session.post(f"{BASE_URL}/api/practice/add-doctor?doctor_id={doctor_id}")
            data = response.json()
            if data.get("success"):
                print(f"  SUCCESS: Added doctor {doctors[0]['name']} to practice.")
                return True
            else:
                print(f"  FAILED: {data}")
                return False
        else:
            print("  SKIPPED: No doctors to add.")
            return True
    else:
        print(f"  FAILED: Search returned {response.status_code}")
        return False

def verify_doctor_join_practice():
    print("--- Verifying Doctor Join Practice API ---")
    session = login("doctor@example.com", "password")
    if not session:
        print("FAILED: Could not login as doctor.")
        return False
    # Search practices
    response = session.get(f"{BASE_URL}/api/practices/search?q=")
    if response.status_code == 200:
        practices = response.json()
        print(f"  Found {len(practices)} practices in search.")
        if len(practices) > 0:
            practice_id = practices[0]["id"]
            # Join practice
            response = session.post(f"{BASE_URL}/api/doctor/join-practice?practice_id={practice_id}")
            data = response.json()
            if data.get("success") or "Already associated" in data.get("error", ""):
                print(f"  SUCCESS: Doctor joined/already in practice {practices[0]['name']}.")
                return True
            else:
                print(f"  FAILED: {data}")
                return False
        else:
            print("  SKIPPED: No practices to join.")
            return True
    else:
        print(f"  FAILED: Search returned {response.status_code}")
        return False

if __name__ == "__main__":
    p = verify_patient_dashboard()
    d = verify_doctor_dashboard()
    pr = verify_practice_dashboard()
    pa = verify_practice_add_doctor()
    dj = verify_doctor_join_practice()
    
    if all([p, d, pr, pa, dj]):
        print("\nALL VERIFICATIONS PASSED.")
    else:
        print("\nSOME VERIFICATIONS FAILED.")
