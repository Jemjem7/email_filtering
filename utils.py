import imaplib
import email
from email.utils import parsedate_to_datetime

def fetch_emails():
    """Fetch emails from your inbox using IMAP."""
    try:
        # Set up the IMAP connection (Replace 'youremail@example.com' and 'password' with actual credentials)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('youremail@example.com', 'password')
        mail.select('inbox')

        # Search and fetch emails
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids:
            result, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Parse email headers
            sender = msg.get("From")
            timestamp = parsedate_to_datetime(msg.get("Date"))
            ip_address = msg.get("X-Originating-IP")  # Optional, may not always exist

            emails.append({
                "subject": msg["subject"],
                "body": msg.get_payload(decode=True).decode(),
                "sender": sender,
                "timestamp": timestamp,
                "ip_address": ip_address,
            })

        return emails
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []
