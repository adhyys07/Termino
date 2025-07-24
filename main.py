from utils.ascii import print_termino_logo
from airtable0 import users
import os
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    print_termino_logo()
    SESSION_FILE = os.path.join(os.path.expanduser("~"), "session.json")
    session = None
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                session = json.load(f)
            # Check if session is still valid (7 days = 604800 seconds)
            if time.time() - session.get("timestamp", 0) < 604800:
                print(f"🎰 Welcome back, {session['username']}! You have {session['coins']} coins.\n")
                dashboard(session)
                return
        except Exception:
            session = None

    while True:
        print("""
========================
| 1. [S]ign Up         |
| 2. [L]ogin           |
| 3. [E]xit            |
========================
        """)
        choice = input("Choose: ").strip().lower()

        if choice == "1" or choice == "s":
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
        elif choice == "2" or choice == "l":
            uname = input("Username: ")
            pwd = input("Password: ")
            user = users.login(uname, pwd)
            if user:
                print(f"🎰 You have {user['coins']} coins.")
                # Save session info
                with open(SESSION_FILE, "w") as f:
                    json.dump({"username": uname, "coins": user["coins"], "timestamp": time.time()}, f)
                dashboard(user)
        elif choice == "3" or choice == "e":
            break

def dashboard(session):
    while True:
        print("\n================ DASHBOARD ================\n")
        print(" [1] 🎰 Slots   |   [2] 🃏 Blackjack   |   [3] 🎯 Roulette   |   [4] 🎲 Craps ")
        print(" [5] 🥇 Wheel of Fortune   |   [6] 💣 Minesweeper   |   [7] 🪃 Plinko   |   [8] 🚪 Logout ")
        print("\n===========================================\n")
        dash_choice = input("Choose an option: ").strip().lower()
        if dash_choice == "1":
            print("Slots game coming soon!")
        elif dash_choice == "2":
            print("Blackjack coming soon!")
        elif dash_choice == "3":
            print("Roulette coming soon!")
        elif dash_choice == "4":
            print("Craps coming soon!")
        elif dash_choice == "5":
            print("Wheel of Fortune coming soon!")
        elif dash_choice == "6":
            print("Minesweeper coming soon!")
        elif dash_choice == "7":
            print("Plinko coming soon!")
        elif dash_choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def send_welcome_email(to_email, username, verification_token):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "adhdhyan.jain@gmail.com"
    sender_password = "iqjzqgnndgfcizqz"
    subject = "Welcome to Termino Casino! Verify your account"
    verification_link = f"http://termino-production.up.railway.app/verify?token={verification_token}"
    body = f"""
Hi {username},

Welcome to Termino Casino! Your account has been created successfully.

Please verify your account by clicking the link below:
{verification_link}

Best regards,
Termino Team
"""
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Verification email sent to {to_email}!")
    except Exception as e:
        print(f" Could not send welcome email: {e}")

if __name__ == "__main__":
    main()