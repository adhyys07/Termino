from utils.ascii import print_termino_logo
from airtable0 import users
import os
import json
import time
import smtplib
from menu import dashboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
    print_termino_logo()
    SESSION_FILE = os.path.join(os.path.expanduser("~"), ".session.json")
    from auth import main as auth_main
    auth_main(SESSION_FILE)

def send_welcome_email(to_email, username, verification_token):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "adhdhyan.jain@gmail.com"
    sender_password = "iqjzqgnndgfcizqz"
    subject = "Welcome to Termino Casino! Verify your account"
    verification_link = f"https://termino.onrender.com/verify?token={verification_token}"
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