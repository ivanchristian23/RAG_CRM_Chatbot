from datetime import datetime
import os
import requests
from dotenv import load_dotenv


load_dotenv()

owner_cache = {}

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

    url = (
        f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/contacts"
        f"?$select=fullname,emailaddress1,jobtitle,telephone1"
        f"&$expand=parentcustomerid_account($select=name)"
    )

    response = requests.get(url, headers=headers)
    print("[DEBUG] Response Status:", response.status_code)

    try:
        json_data = response.json()
        print("[DEBUG] Response JSON Sample:", json_data.get("value", [])[:1])
    except Exception as e:
        print("[ERROR] Failed to parse JSON:", e)
        return []

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
        company = c.get("parentcustomerid_account") or {}
        company_name = company.get("name", "N/A")


        contact_text = f"""
        Name: {name}
        Email: {email}
        Job Title: {job}
        Business Phone: {phone}
        Company: {company_name}
        """.strip()

        results.append(contact_text)

    print(f"[INFO] Prepared {len(results)} contact records for vector store.")
    return results

def resolve_owner_name(owner_id):
    if not owner_id:
        return "N/A"

    # Check if we've already resolved this owner
    if owner_id in owner_cache:
        return owner_cache[owner_id]

    # Call the Dynamics API to fetch owner's fullname
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/systemusers({owner_id})?$select=fullname"
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            name = r.json().get("fullname", "Unknown User")
            owner_cache[owner_id] = name
            return name
        else:
            print(f"[WARN] Failed to resolve owner {owner_id}: {r.status_code} - {r.text}")
            return "Unknown User"
    except Exception as e:
        print(f"[ERROR] Exception resolving owner {owner_id}: {str(e)}")
        return "Unknown User"    

def get_accounts():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = (
        f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/accounts"
        f"?$select=name,accountnumber,industrycode,telephone1,websiteurl"
    )

    response = requests.get(url, headers=headers)
    print("[DEBUG] Account Response Status:", response.status_code)

    try:
        json_data = response.json()
        print("[DEBUG] Account Sample:", json_data.get("value", [])[:1])
    except Exception as e:
        print("[ERROR] Failed to parse JSON for accounts:", e)
        return []

    if "value" not in json_data:
        print("[ERROR] No 'value' key in account response.")
        return []

    data = json_data["value"]
    results = []

    for acc in data:
        name = acc.get("name", "N/A")
        number = acc.get("accountnumber", "N/A")
        industry = acc.get("industrycode", "N/A")
        phone = acc.get("telephone1", "N/A")
        website = acc.get("websiteurl", "N/A")

        account_text = f"""
        Account Name: {name}
        Account Number: {number}
        Industry: {industry}
        Phone: {phone}
        Website: {website}
        """.strip()

        results.append(account_text)

    print(f"[INFO] Prepared {len(results)} account records for vector store.")
    return results

def get_activities():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = (
        f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/activitypointers"
        f"?$select=subject,activitytypecode,actualstart,actualend"
        f"&$expand=ownerid"
        f"&$top=50"
    )

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("[ERROR] Failed to get activities:", r.text)
        return []

    data = r.json().get("value", [])
    results = []

    for a in data:
        subject = a.get("subject", "N/A")
        type_ = a.get("activitytypecode", "N/A")
        start = a.get("actualstart", "N/A")
        end = a.get("actualend", "N/A")
        owner_info = a.get("ownerid", {})
        owner_id = owner_info.get("ownerid")
        owner_name = resolve_owner_name(owner_id) if owner_id else "N/A"

        activity_text = f"""
        Activity Type: {type_}
        Subject: {subject}
        Start: {start}
        End: {end}
        Owner: {owner_name}
        """.strip()
        results.append(activity_text)

    print(f"[INFO] Retrieved {len(results)} activities.")
    return results

def get_leads():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = (
        f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/leads"
        f"?$select=fullname,companyname,emailaddress1,statuscode,subject,createdon"
        f"&$expand=owninguser($select=fullname)"
        f"&$top=50"
    )

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("[ERROR] Failed to get leads:", r.text)
        return []
    try:
        json_data = r.json()
        print("[DEBUG] Leads Sample:", json_data.get("value", [])[:1])
    except Exception as e:
        print("[ERROR] Failed to parse JSON for accounts:", e)
        return []

    if "value" not in json_data:
        print("[ERROR] No 'value' key in account response.")
        return []

    data = r.json().get("value", [])
    results = []

    status_map = {
        0: "Disqualified",
        1: "New Lead",
        2: "Contacted",
        3: "Qualified",
        4: "Converted",
    }

    for l in data:
        name = l.get("fullname", "N/A")
        owner_data = l.get("owninguser")
        owner_name = owner_data.get("fullname") if owner_data else "N/A"
        # topic = l.get("topic", "N/A")
        company = l.get("companyname", "N/A")
        email = l.get("emailaddress1", "N/A")
        status_code = l.get("statuscode")
        status = status_map.get(status_code, f"Unknown ({status_code})")
        subject = l.get("subject", "N/A")
        createdon_raw = l.get("createdon", "")
        datetime_object = datetime.strptime(createdon_raw, "%Y-%m-%dT%H:%M:%SZ")
        # Example: Format to "March 05, 2025 11:54 AM"
        formatted_string = datetime_object.strftime("%B %d, %Y")
        monthofdate = datetime_object.strftime("%B")
        print(formatted_string)


        lead_text = f"""
        [Lead]
        Subject: {subject}
        Contact Lead Name: {name}
        Company: {company}
        Email: {email}
        Status: {status}
        Owner: {owner_name}
        Created On: {formatted_string}
        Month: {monthofdate}

        """.strip()
        results.append(lead_text)

    print(f"[INFO] Retrieved {len(results)} leads.")
    return results

def get_opportunities():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = (
        f"{os.getenv('DYNAMICS_URL')}/api/data/v9.2/opportunities"
        f"?$select=name,estimatedvalue,estimatedclosedate,statecode"
        f"&$expand=owninguser($select=fullname)"
        f"&$top=50"
    )

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("[ERROR] Failed to get opportunities:", r.text)
        return []

    data = r.json().get("value", [])
    results = []

    for o in data:
        name = o.get("name", "N/A")
        value = o.get("estimatedvalue", "N/A")
        close_date = o.get("estimatedclosedate", "N/A")
        status = o.get("statecode", "N/A")
        owner = o.get("owninguser", {})
        owner_name = owner.get("fullname", "N/A")

        opportunity_text = f"""
        [Opportunity]
        Opportunity: {name}
        Estimated Value: {value}
        Expected Close: {close_date}
        Status Code: {status}
        Owner: {owner_name}
        """.strip()
        results.append(opportunity_text)

    print(f"[INFO] Retrieved {len(results)} opportunities.")
    return results
