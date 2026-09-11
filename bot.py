import os
import smtplib
from email.message import EmailMessage
import requests
import yfinance as yf
import pandas as pd

# 1. Telegram Alert Function
def send_telegram_alert(report_text):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Telegram credentials nahi mile!")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": report_text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram par report bhej di gayi hai! 🚀")
        else:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Exception: {e}")

# 2. Email Alert Function
def send_email_alert(report_text):
    sender_email = "your_email@gmail.com" # Yahan apna email daal dein
    receiver_email = "your_email@gmail.com" # Jisko bhejna hai uska email
    app_password = os.environ.get("MAIL_PASS") # Jo GitHub Secrets mein save hai
    
    if not app_password:
        print("Email App Password nahi mila!")
        return

    msg = EmailMessage()
    msg.set_content(report_text)
    msg['Subject'] = "📈 Daily Active Stock Signals Report"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Email par report bhej di gayi hai! 📧")
    except Exception as e:
        print(f"Email Exception: {e}")

# 50 Stocks List
symbols = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "SBIN.NS", 
    "BHARTIARTL.NS", "ITC.NS", "TATAMOTORS.NS", "KOTAKBANK.NS", "LT.NS", 
    "HINDUNILVR.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS", 
    "TITAN.NS", "BAJFINANCE.NS", "HCLTECH.NS", "TATASTEEL.NS", "NTPC.NS", 
    "POWERGRID.NS", "M&M.NS", "ADANIENT.NS", "COALINDIA.NS", "BAJAJFINSV.NS", 
    "GRASIM.NS", "TECHM.NS", "HINDALCO.NS", "WIPRO.NS", "ULTRACEMCO.NS", 
    "ONGC.NS", "JSWSTEEL.NS", "ADANIPORTS.NS", "TATACONSUMER.NS", "BRITANNIA.NS", 
    "DRREDDY.NS", "CIPLA.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "SBILIFE.NS", 
    "HDFCLIFE.NS", "BPCL.NS", "DIVISLAB.NS", "LTIM.NS", "BEL.NS", 
    "PIDILITIND.NS", "APOLLOHOSP.NS", "HAVELLS.NS", "INDUSINDBK.NS", "BAJAJ-AUTO.NS", 
    "TRENT.NS", "NESTLEIND.NS"
]

report_summary = "🚨 Aaj ke Active Filtered Stock Signals & Stop-Loss:\n\n"
active_signals_found = False

print("... Market scan ho raha hai...\n")

for symbol in symbols:
    try:
        stock_data = yf.download(symbol, period="90d", interval="1d", progress=False)
        if stock_data.empty or len(stock_data) < 60:
            continue
            
        close = stock_data['Close']
        latest_price = float(close.iloc[-1].item())
        ma_50 = float(close.rolling(window=50).mean().iloc[-1].item())
        
        # RSI Calculation (14 periods)
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0.0)
        avg_gain = float(gain.rolling(window=14).mean().iloc[-1].item())
        avg_loss = float(loss.rolling(window=14).mean().iloc[-1].item())
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
        clean_name = symbol.replace(".NS", "")
        
        # Filter Logic
        if latest_price > ma_50 and rsi > 55:
            stop_loss = latest_price * 0.98
            signal = f"BUY : {clean_name} | Price: {latest_price:.2f} | 50MA: {ma_50:.2f} | RSI: {rsi:.1f} | SL: {stop_loss:.2f}\n"
            report_summary += signal
            active_signals_found = True
        elif latest_price < ma_50 and rsi < 45:
            stop_loss = latest_price * 1.02
            signal = f"SELL : {clean_name} | Price: {latest_price:.2f} | 50MA: {ma_50:.2f} | RSI: {rsi:.1f} | SL: {stop_loss:.2f}\n"
            report_summary += signal
            active_signals_found = True
            
    except Exception as e:
        continue

if not active_signals_found:
    report_summary += "Aaj koi bhi strong active signal match nahi hua hai.\n"

report_summary += "\n---\nBot automated for Jyoti ✨"

# Dono jagah ek sath bhej do
send_telegram_alert(report_summary)
send_email_alert(report_summary)
print("Dono jagah report successfully bhej di gayi hai!")
