"""
This script automates the process of sending and receiving emails.
It sends a scheduled reminder email every day and checks for recent emails in the inbox.
"""

import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import schedule
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS")
RECIPIENT_PASSWORD = os.getenv("RECIPIENT_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT"))


# Send Email

def send_email(recipient_address, subject, body):
    """Function to send an email."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_address, msg.as_string())
        print(f"Email sent to {recipient_address}")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

# Recieve Email

def receive_email():
    """Function to receive emails."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(RECIPIENT_ADDRESS, RECIPIENT_PASSWORD)
        mail.select('inbox')

        status, messages = mail.search(None, 'ALL')
        if status == 'OK':
            email_ids = messages[0].split()

            for email_id in email_ids[-3:]:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            print(f"From: {msg['from']}")
                            print(f"Subject: {msg['subject']}")
                            
                            # Handle multipart email content
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        print("Plain Text Body:", body)
                                    elif content_type == "text/html":
                                        html_body = part.get_payload(decode=True).decode()
                                        print("HTML Body:", html_body)
                            else:
                                # For emails with only one part (non-multipart)
                                body = msg.get_payload(decode=True).decode()
                                print("Body:", body)
        mail.logout()
    except imaplib.IMAP4.error as e:
        print(f"Error receiving email: {e}")



# Job functions to be scheduled
def email_reminder_job():
    """Job function for sending an email reminder."""
    send_email(RECIPIENT_ADDRESS, "Scheduled Reminder", "This is your scheduled email reminder.")
    receive_email()


# Schedule the jobs
schedule.every().day.at("23:08").do(email_reminder_job)  # Email at 23:08 PM every day



# Main loop to keep the scheduler running
print("Scheduler is running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
