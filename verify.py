from flask import Flask, request, render_template_string
import os
import requests
from airtable0.airtable_config import BASE_ID, TABLE_NAME, HEADERS

API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

app = Flask(__name__)

@app.route('/verify')
def verify():
    token = request.args.get('token')
    if not token:
        return "Invalid verification link.", 400

    params = {"filterByFormula": f"VerificationToken='{token}'"}
    response = requests.get(API_URL, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    if not records:
        return "Invalid or expired verification link.", 404

    user_id = records[0]["id"]
    data = {"fields": {"Verified": True}}
    update_res = requests.patch(f"{API_URL}/{user_id}", headers=HEADERS, json=data)
    if update_res.status_code == 200:
        return render_template_string("<h2>✅ Your account has been verified! You can now log in.</h2>")
    else:
        return "Failed to verify account.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))