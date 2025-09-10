"""Send Email using SMTP"""
import smtplib
from email.mime.text import MIMEText

def send_email(sender, password, recipient, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
        print("Email sent successfully!")

if __name__ == "__main__":
    print("This script sends email using SMTP. Configure credentials before running.")
