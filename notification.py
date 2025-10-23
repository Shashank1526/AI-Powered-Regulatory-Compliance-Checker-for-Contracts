import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import requests

load_dotenv()

SENDER = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("SENDER_PASSWORD")  # use Gmail App Password
RECEIVER = os.getenv("RECEIVER_EMAIL")

def send_notification(subject, notification):
    
    try:
        sender=SENDER
        password=PASSWORD
        receiver=RECEIVER


        # create message
        msg = MIMEText(f"{notification}")
        msg["Subject"]=subject
        msg["From"]=sender
        msg["To"]= receiver


        #connect to the Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() #start TLS encrytion
            server.login(sender, password)
            server.send_message(msg)
            
        print("Email sent Successfully!")
        
    except Exception as e:
        print("Error Occured",e)

    # send slack notification

    SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

    try:
        webhook_url = SLACK_WEBHOOK
        payload = {
            "text": f"*{subject}*\n{notification}",
            "username": "ComplianceBot 🕵️‍♂️",
            "icon_emoji": ":shield:",
        }
        res = requests.post(webhook_url, json=payload, timeout=10)
        res.raise_for_status()
        print("Slack notification sent.")
    except Exception as e:
        print("Slack notification error:", e)