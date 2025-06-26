import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_token():
    url = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token"
    data = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type': 'client_credentials',
        'scope': f"{os.getenv('DYNAMICS_URL')}/.default"
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()['access_token']

def get_contacts():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/contacts?$select=fullname,emailaddress1,jobtitle,telephone1"

    response = requests.get(url, headers=headers)
    print("[DEBUG] Response Status:", response.status_code)
    json_data = response.json()
    print("[DEBUG] Response JSON:", json_data)

    if "value" not in json_data:
        print("[ERROR] No 'value' key in response. Full response:", json_data)
        return []

    data = json_data["value"]

    results = []
    for c in data:
        name = c.get("fullname", "N/A")
        email = c.get("emailaddress1", "N/A")
        job = c.get("jobtitle", "N/A")
        phone = c.get("telephone1", "N/A")

        contact_text = f"""
        Name: {name}
        Email: {email}
        Job Title: {job}
        Business Phone: {phone}
        """.strip()

        results.append(contact_text)

    print(f"[DEBUG] Prepared {len(results)} contact entries for vector store.")
    return results
