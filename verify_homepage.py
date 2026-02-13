import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8001"

def login(email, password):
    session = requests.Session()
    login_url = f"{BASE_URL}/login/"
    response = session.post(login_url, data={"email": email, "password": password})
    print(f"Login Response URL: {response.url}")
    print(f"Login Response Status: {response.status_code}")
    if response.url.rstrip("/") == f"{BASE_URL}": # Handling potential trailing slash mismatch
        return session
    return None

def verify_patient_homepage():
    print("--- Verifying Patient Homepage ---")
    session = login("patient@example.com", "password")
    if not session:
        print("FAILED: Could not login as patient.")
        return False

    response = session.get(f"{BASE_URL}/")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for Tabs
    doctors_tab = soup.find('button', id='pills-doctors-tab')
    practices_tab = soup.find('button', id='pills-practices-tab')

    if doctors_tab and practices_tab:
        print("SUCCESS: Doctors and Practices tabs found.")
    else:
        print("FAILED: Tabs not found.")
        return False

    # Check for Doctor Entry (Doc Doctor) -> Slug: Doc_Doctor
    doc_link = soup.find('a', href='/Doc_Doctor')
    if doc_link:
        print("SUCCESS: Link to Doc_Doctor found.")
    else:
        print("FAILED: Link to Doc_Doctor not found.")
        print("--- HTML Dump (Doctors Tab) ---")
        doctors_tab_content = soup.find('div', id='pills-doctors')
        print(doctors_tab_content)
        with open("debug_homepage.html", "w") as f:
            f.write(response.text)
        return False

    # Check for Practice Entry (City Dental) -> Slug: City_Dental
    practice_link = soup.find('a', href='/City_Dental')
    if practice_link:
        print("SUCCESS: Link to City_Dental found.")
    else:
        print("FAILED: Link to City_Dental not found.")
        return False

    return True

def verify_profiles():
    print("--- Verifying Profiles ---")
    session = login("patient@example.com", "password")
    
    # Doctor Profile
    doc_url = f"{BASE_URL}/Doc_Doctor"
    response = session.get(doc_url)
    doc_url = f"{BASE_URL}/Doc_Doctor"
    response = session.get(doc_url)
    if response.status_code == 200 and "Doc Doctor" in response.text:
        print(f"SUCCESS: Doctor profile loaded correctly at {doc_url}")
    else:
        print(f"FAILED: Doctor profile failed. Status: {response.status_code}")
        return False

    # Practice Profile
    practice_url = f"{BASE_URL}/City_Dental"
    response = session.get(practice_url)
    if response.status_code == 200 and "City Dental" in response.text and "Address" in response.text:
        print(f"SUCCESS: Practice profile loaded correctly at {practice_url}")
    else:
        print(f"FAILED: Practice profile failed. Status: {response.status_code}")
        return False

    return True

if __name__ == "__main__":
    if verify_patient_homepage() and verify_profiles():
        print("\nALL CHECKS PASSED.")
    else:
        print("\nSOME CHECKS FAILED.")
