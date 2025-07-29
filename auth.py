
import time
import base64
import subprocess
from airtable0 import users
from menu import dashboard
import os
import json

def auto_login(SESSION_FILE):
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "rb") as f:
                encoded = f.read()
            if not encoded:
                print("Auto-login failed: session file is empty.")
                return False
            try:
                session_data = base64.b64decode(encoded)
                session = json.loads(session_data.decode())
            except Exception:
                print("Auto-login failed: session file is corrupted.")
                return False
            uname = session.get("username")
            pwd = session.get("password")
            if not uname or not pwd:
                print("Auto-login failed: missing credentials in session file.")
                return False
            user = users.login(uname, pwd)
            if user:
                print(f"🔑 Auto-logged in as {uname}!")
                dashboard(user)
                return True
            else:
                print("Auto-login failed: invalid credentials.")
        except Exception as e:
            print(f"Auto-login failed: {e}")
    return False

def signup_flow(SESSION_FILE):
    while True:
        uname = input("Username: ").strip()
        email = input("Email: ").strip()
        pwd = input("Password: ").strip()
        if not uname or not email or not pwd:
            print("❌ Username, email, and password cannot be empty.")
            continue
        if "@" not in email:
            print("❌ Email must contain '@'.")
            continue
        break
    signup_success = users.signup(uname, pwd, email)
    if signup_success:
        print("Please check your email for a verification link.")

def login_flow(SESSION_FILE):
    uname = input("Username: ")
    pwd = input("Password: ")
    user = users.login(uname, pwd)
    if user:
        print(f"🎰 You have {user['coins']} coins.")
        session_data = json.dumps({
            "username": uname,
            "password": pwd,
            "timestamp": time.time()
        }).encode()
        encoded = base64.b64encode(session_data)
        with open(SESSION_FILE, "wb") as f:
            f.write(encoded)
        dashboard(user)

def main(SESSION_FILE):
    if auto_login(SESSION_FILE):
        return
    while True:
        print("Welcome to Termino Casino!")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            signup_flow(SESSION_FILE)
        elif choice == "2":
            login_flow(SESSION_FILE)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
