import tkinter as tk
from tkinter import messagebox
from filter import filter_email, send_filtered_email
from utils import fetch_emails

# Function to display email details in a separate window
def inspect_email(subject, sender, timestamp, ip_address):
    email_details = f"Subject: {subject}\nFrom: {sender}\nTime: {timestamp}\nIP Address: {ip_address}"
    details_window = tk.Toplevel(root)
    details_window.title("Email Details")
    tk.Label(details_window, text=email_details).pack(padx=20, pady=20)

# Function to display emails and set up the inspect button
def display_emails():
    emails = fetch_emails()  # Fetch emails
    for email_data in emails:
        email_display = f"Subject: {email_data['subject']} - From: {email_data['sender']}"
        emails_list.insert(tk.END, email_display)

        # Create inspect button for each email
        inspect_button = tk.Button(root, text="Inspect", command=lambda e=email_data: inspect_email(e['subject'], e['sender'], e['timestamp'], e['ip_address']))
        emails_list.itemconfig(emails_list.size() - 1, {'bg': 'lightgray'})  # Alternating row colors
        emails_list.insert(tk.END, email_display)  # Add inspect button next to the email
        inspect_button.pack()

# Tkinter setup for the user interface
root = tk.Tk()
root.title("Email Filtering System")

# Listbox to display fetched emails
emails_list = tk.Listbox(root, width=80, height=15)
emails_list.pack(padx=10, pady=10)

# Email filtering input fields
tk.Label(root, text="Subject:").pack()
entry_subject = tk.Entry(root, width=50)
entry_subject.pack(padx=10, pady=5)

tk.Label(root, text="Body:").pack()
entry_body = tk.Text(root, height=10, width=50)
entry_body.pack(padx=10, pady=5)

# Filter Button to check the email
filter_button = tk.Button(root, text="Filter Email", command=lambda: filter_email(entry_subject.get(), entry_body.get()))
filter_button.pack(pady=10)

# Load emails button
load_emails_button = tk.Button(root, text="Load Emails", command=display_emails)
load_emails_button.pack(pady=10)

root.mainloop()
