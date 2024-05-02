from dotenv import load_dotenv
from email_receiver import EmailReader
import requests
import os

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
EMAIL_SENDERS = os.environ.get("EMAIL_SENDERS").split(",")
for i in range(1, 5):

    email_address = os.environ.get(f"EMAIL_{i}")
    password = os.environ.get(f"PASSWORD_{i}")

    if email_address and password:
        email_reader = EmailReader(email_address, password)
        unread_emails = email_reader.read_unseen_email_from(EMAIL_SENDERS)
        for email in unread_emails:
            url = f"http://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={email}"
            response = requests.get(url)

        email_reader.logout()
