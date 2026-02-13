import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8001"

def login(email, password):
    session = requests.Session()
    login_url = f"{BASE_URL}/login/"
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
        print(response.text[:500])
        return False

def verify_doctor_dashboard():
    print("--- Verifying Doctor Dashboard ---")
    session = login("doctor@example.com", "password")
    if not session:
        print("FAILED: Could not login as doctor.")
        return False
    
    response = session.get(f"{BASE_URL}/")
    if "Welcome to No Pain" in response.text and "You are logged in as a <strong>Doctor</strong>" in response.text:
        print("SUCCESS: Doctor dashboard loaded correctly.")
        return True
    else:
        print("FAILED: Doctor dashboard content mismatch.")
        print(response.text[:500])
        return False

def verify_practice_dashboard():
    print("--- Verifying Practice Dashboard ---")
    session = login("practice@example.com", "password")
    if not session:
        print("FAILED: Could not login as practice.")
        return False
    
    response = session.get(f"{BASE_URL}/")
    if "Welcome to No Pain" in response.text and "You are logged in as a <strong>Practice</strong>" in response.text:
        print("SUCCESS: Practice dashboard loaded correctly.")
        return True
    else:
        print("FAILED: Practice dashboard content mismatch.")
        print(response.text[:500])
        return False

if __name__ == "__main__":
    p = verify_patient_dashboard()
    d = verify_doctor_dashboard()
    pr = verify_practice_dashboard()
    
    if p and d and pr:
        print("\nALL DASHBOARDS VERIFIED.")
    else:
        print("\nVERIFICATION FAILED.")
