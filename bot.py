import os
import smtplib
import time
from email.message import EmailMessage
import pandas as pd
from nselib import capital_market

def send_email_alert(report_text):
    sender_email = "abhay7414998710@gmail.com"
    app_password = os.environ.get("MAIL_PASS")  # GitHub ke secrets se password lega
    
    msg = EmailMessage()
    msg.set_content(report_text)
    msg.subject = "🚨 Top NSE Stocks Daily Scan Report!"
    msg['From'] = sender_email
    msg['To'] = sender_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Report successfully email par bhej di gayi hai! 📧")
    except Exception as e:
        print(f"Error: {e}")

# Top stocks ki list
symbols = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "SBIN", "BHARTIARTL", 
    "ITC", "TATAMOTORS", "KOTAKBANK", "LT", "HINDUNILVR", "AXISBANK", 
    "ASIANPAINT", "MARUTI", "SUNPHARMA", "TITAN", "BAJFINANCE", "HCLTECH", 
    "TATASTEEL", "NTPC", "POWERGRID", "M&M", "ADANIENT", "COALINDIA", 
    "BAJAJFINSV", "GRASIM", "TECHM", "HINDALCO", "WIPRO", "ULTRACEMCO", 
    "ONGC", "JSWSTEEL", "ADANIPORTS", "TATACONSUMER", "BRITANNIA", 
    "DRREDDY", "CIPLA", "EICHERMOT", "HEROMOTOCO", "SBILIFE", "HDFCLIFE", 
    "BPCL", "DIVISLAB", "LTIM", "BEL", "PIDILITIND", "APOLLOHOSP", 
    "HAVELLS", "INDUSINDBK", "BAJAJ-AUTO", "TRENT", "NESTLEIND"
]

report_summary = "Aaj ka Top 50+ Stocks Live Scan Result:\n\n"
print("... Market scan ho raha hai...\n")

for symbol in symbols:
    try:
        time.sleep(1)
        data = capital_market.price_volume_and_deliverable_position_data(symbol=symbol, from_date='01-01-2026', to_date='08-09-2026')
        
        if data is None or data.empty:
            continue
            
        data['ClosePrice'] = data['ClosePrice'].astype(str).str.replace(',', '').astype(float)
        latest_price = data['ClosePrice'].iloc[-1]
        ma_50 = data['ClosePrice'].rolling(window=50).mean().iloc[-1]
        
        if latest_price > ma_50:
            signal = f"🟢 BUY : {symbol} | Price: {latest_price:.2f} | 50 MA: {ma_50:.2f}\n"
        else:
            signal = f"🔴 SELL : {symbol} | Price: {latest_price:.2f} | 50 MA: {ma_50:.2f}\n"
            
        print(signal)
        report_summary += signal
        
    except Exception as e:
        print(f"⚠️ {symbol} ka data skip ho gaya.")

report_summary += "\n---\nBot automated by Jyoti"
send_email_alert(report_summary)
print("\nScan aur Email bhejne ka kaam poora ho gaya! 📊📧")
