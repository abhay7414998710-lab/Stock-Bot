import os
import smtpd
import smtplib
from email.message import EmailMessage
import pandas as pd
from nselib import capital_market

def send_email_alert(report_text):
    sender_email = "abhay7414998710@gmail.com"
    app_password = os.environ.get("MAIL_PASS")  # Yeh GitHub ke secret se password le lega

    msg = EmailMessage()
    msg.set_content(report_text)
    msg.subject = "📈 NSE Live Stock Alert Report!"
    msg['From'] = sender_email
    msg['To'] = sender_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Asli market report email par bhej di gayi hai!")
    except Exception as e:
        print(f"Error: {e}")

# Stocks ki list aur baaki logic yahan aage add rahega
symbols = ["RELIANCE", "TCS", "INFY"] # Aapke baaki stocks
report_summary = "Aaj ka NSE Live Scan Result:\n\n"

# (Aapka baaki code jo 50-day MA aur alert banata hai)
