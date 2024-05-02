from dotenv import load_dotenv
from typing import List
import imaplib
import email

load_dotenv()


class EmailReader:
    def __init__(self, email_address, password):
        self.imap_server = "imap.gmail.com"
        self.email_address = email_address
        self.password = password
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.logged_in = False

    def login(self):
        try:
            self.imap.login(self.email_address, self.password)
            self.logged_in = True
            return True
        except imaplib.IMAP4.error as e:
            print("Login failed: ", str(e))
            return False

    def read_unseen_email_from(self, email_senders: List[str]):
        if not self.logged_in:
            if not self.login():
                return False

        unseen_emails = []

        try:
            for sender in email_senders:
                self.imap.select("inbox")
                search_criteria = f'(UNSEEN FROM "{sender}")'
                _, msgnums = self.imap.search(None, search_criteria)

                for msgnum in msgnums[0].split():
                    _, data = self.imap.fetch(msgnum, "RFC822")
                    message = email.message_from_bytes(data[0][1])
                    email_json = f"""
                                From: {message.get("From")}\n,
                                To: {message.get("To")}\n,
                                BCC: {message.get("BCC")}\n,
                                Date: {message.get("Date")}\n,
                                Subject: {message.get("Subject")}\n
                                """

                    unseen_emails.append(email_json)
        except imaplib.IMAP4.error as e:
            print("Error reading email: ", str(e))
        finally:
            return unseen_emails

    def logout(self):
        if self.logged_in:
            self.imap.close()
            self.logged_in = False
