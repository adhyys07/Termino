import requests
import hashlib
from airtable0.airtable_config import BASE_ID, TABLE_NAME, HEADERS
import uuid

API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password, email):
    verification_token = str(uuid.uuid4())
    # Check if username exists
    response = requests.get(API_URL, headers=HEADERS, params={"filterByFormula": f"Username='{username}'"})
    if response.status_code != 200:
        print("❌ Error checking username:", response.status_code, response.text)
        return False
    if response.json().get("records"):
        print("❌ Username already exists.")
        return False

    data = {
        "fields": {
            "Username": username,
            "PasswordHash": hash_password(password),
            "Email": email,
            "Coins": 1000,
            "Verified": False,
            "VerificationToken": verification_token
        }
    }
    res = requests.post(API_URL, headers=HEADERS, json=data)
    if res.status_code == 200:
        print("✅ Account created successfully!")
        import main
        main.send_welcome_email(email, username, verification_token)
        return True
    else:
        print("❌ Error creating account.")
        print(res.status_code, res.text)
        return False

def login(username, password):
    response = requests.get(API_URL, headers=HEADERS, params={"filterByFormula": f"Username='{username}'"})
    if response.status_code != 200:
        print("❌ Error fetching user:", response.status_code, response.text)
        return None
    records = response.json().get("records", [])
    if not records:
        print("Username not found.")
        return None

    record = records[0]
    stored_hash = record["fields"].get("PasswordHash")
    if hash_password(password) == stored_hash:
        email = record["fields"].get("Email", "")
        print(f"✅ Welcome {username}! You have {record['fields'].get('Coins', 0)} coins.")
        return {"id": record["id"], "username": username, "email": email, "coins": record["fields"].get("Coins", 0)}
    else:
        print("Incorrect password.")
        return None

def update_coins(user_id, new_coin_value):
    url = f"{API_URL}/{user_id}"
    data = {
        "fields": {
            "Coins": new_coin_value
        }
    }
    res = requests.patch(url, headers=HEADERS, json=data)
    if res.status_code != 200:
        print("❌ Error updating coins:", res.status_code, res.text)
    return res.status_code == 200