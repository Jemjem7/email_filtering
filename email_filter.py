import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
import imaplib
import email

# Initialize global variable to hold the suspicious email data
suspicious_email = {}

def filter_email(subject, body):
    """Basic email filtering logic for phishing/spam detection"""
    
    suspicious_keywords = [
        'urgent', 'claim your prize', 'click here', 'free gift',
        'limited time offer', 'congratulations', 'act now', 'exclusive deal',
        'winner', 'unsecured', 'verify your account', 'click to claim',
        'account blocked', 'immediate action required', 'claim your reward',
        'important update', 'unclaimed prize'
    ]
    
    safe_keywords = [
        'meeting scheduled', 'invoice', 'order confirmation', 'payment received',
        'subscription confirmed', 'your receipt', 'welcome back', 'service update',
        'account activity', 'monthly report', 'project update', 'hello', 'request for information'
    ]
    
    # Check for suspicious keywords in the email body
    for keyword in suspicious_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', body, re.IGNORECASE):
            return "Suspicious"
    
    # Check for safe keywords in the email body
    for keyword in safe_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', body, re.IGNORECASE):
            return "Safe"
    
    # Default result if no match for either category
    return "Unknown"


def send_filtered_email(recipient, subject, body, status, sender, timestamp, ip_address):
    """Send filtered email notification with sender details"""
    msg = MIMEMultipart()
    msg['From'] = 'youremail@example.com'
    msg['To'] = recipient
    msg['Subject'] = f"Email Status: {status} - {subject}"

    body_message = f"Sender: {sender}\nDate: {timestamp}\nIP Address: {ip_address}\n\nEmail Body:\n{body}"
    msg.attach(MIMEText(body_message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('youremail@example.com', 'password')
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        print(f"Filtered email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def fetch_emails():
    """Fetch emails from your inbox (IMAP example)"""
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('youremail@example.com', 'password')
        mail.select('inbox')

        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids:
            result, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            emails.append({
                "subject": msg["subject"],
                "body": msg.get_payload(decode=True).decode(),
                "sender": msg["from"],
                "timestamp": msg["date"],
                "ip_address": "192.168.1.1"  # Example static IP, can be replaced with dynamic if needed
            })

        return emails
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

# Tkinter setup
root = tk.Tk()
root.title("Email Filtering System")

# Email filtering input fields and labels
tk.Label(root, text="Subject:").pack()
entry_subject = tk.Entry(root, width=50)
entry_subject.pack()

tk.Label(root, text="Body:").pack()
entry_body = tk.Text(root, height=10, width=50)
entry_body.pack()

# Result display label
result_label = tk.Label(root, text="Email Status: ")
result_label.pack()

# Inspect button (hidden initially)
inspect_button = tk.Button(root, text="Inspect", command=lambda: open_inspect_window(), state=tk.DISABLED)
inspect_button.pack()

# Function to open Inspect Window
def open_inspect_window():
    """Opens a window to inspect suspicious email"""
    if suspicious_email:
        subject = suspicious_email['subject']
        body = suspicious_email['body']
        sender = suspicious_email['sender']
        timestamp = suspicious_email['timestamp']
        ip_address = suspicious_email['ip_address']

        # Create inspect window and populate email details
        inspect_window = Toplevel(root)
        inspect_window.title("Inspect Suspicious Email")

        email_details = f"Subject: {subject}\nBody: {body}\nSender: {sender}\nTimestamp: {timestamp}\nIP Address: {ip_address}"
        label_details = tk.Label(inspect_window, text=email_details, justify=tk.LEFT)
        label_details.pack()
    else:
        messagebox.showwarning("No Suspicious Email", "No suspicious email detected.")

# Filter button action
def on_filter_email():
    """Triggers the email filtering process"""
    subject = entry_subject.get()
    body = entry_body.get("1.0", tk.END).strip()  # Get all text in Text widget

    status = filter_email(subject, body)
    result_label.config(text=f"Email Status: {status}")
    
    if status == "Suspicious":
        # Store suspicious email data for inspection
        suspicious_email['subject'] = subject
        suspicious_email['body'] = body
        suspicious_email['sender'] = "sender@example.com"  # Update with real sender if needed
        suspicious_email['timestamp'] = "2025-02-23 14:30"  # Update with real timestamp
        suspicious_email['ip_address'] = "192.168.1.1"  # Example IP address, should be dynamically updated if possible

        send_filtered_email('recipient@example.com', subject, body, status, suspicious_email['sender'], suspicious_email['timestamp'], suspicious_email['ip_address'])
        messagebox.showwarning("Suspicious Email", "This email is suspicious!")
        
        # Enable Inspect button after detecting suspicious email
        inspect_button.config(state=tk.NORMAL)
    else:
        messagebox.showinfo("Safe Email", "This email seems safe.")

filter_button = tk.Button(root, text="Filter Email", command=on_filter_email)
filter_button.pack()

# Run the Tkinter event loop
root.mainloop()
