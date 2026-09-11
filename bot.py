import os
import smtplib
from email.message import EmailMessage
import yfinance as yf
import pandas as pd

def send_email_alert(report_text):
    sender_email = "abhay7414998710@gmail.com"
    app_password = os.environ.get("MAIL_PASS")
    
    msg = EmailMessage()
    msg.set_content(report_text)
    msg.subject = "🚨 Active Smart Stock Signals & Stop-Loss Report!"
    msg['From'] = sender_email
    msg['To'] = sender_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Filtered active report email par bhej di gayi hai! 📧")
    except Exception as e:
        print(f"Error: {e}")

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

report_summary = "Aaj ke Active Filtered Stock Signals & Stop-Loss:\n\n"
active_signals_found = False

print("... Market scan ho raha hai...\n")

for symbol in symbols:
    try:
        stock_data = yf.download(symbol, period="90d", interval="1d", progress=False)
        if stock_data.empty or len(stock_data) < 60:
            continue
            
        close = stock_data['Close']
        latest_price = float(close.iloc[-1])
        ma_50 = float(close.rolling(window=50).mean().iloc[-1])
        
        # RSI Calculation (14 periods)
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0.0)
        avg_gain = gain.rolling(window=14).mean().iloc[-1]
        avg_loss = loss.rolling(window=14).mean().iloc[-1]
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
        clean_name = symbol.replace(".NS", "")
        
        # Filter Logic: Sirf wahi stocks aayenge jinka RSI aur Moving Average strong active signal de raha ho
        if latest_price > ma_50 and rsi > 55:
            stop_loss = latest_price * 0.98
            signal = f"🟢 BUY : {clean_name} | Price: {latest_price:.2f} | 50MA: {ma_50:.2f} | RSI: {rsi:.1f} | SL: {stop_loss:.2f}\n"
            report_summary += signal
            active_signals_found = True
        elif latest_price < ma_50 and rsi < 45:
            stop_loss = latest_price * 1.02
            signal = f"🔴 SELL : {clean_name} | Price: {latest_price:.2f} | 50MA: {ma_50:.2f} | RSI: {rsi:.1f} | SL: {stop_loss:.2f}\n"
            report_summary += signal
            active_signals_found = True
            
    except Exception as e:
        continue

if not active_signals_found:
    report_summary += "Aaj koi bhi strong active signal match nahi hua hai.\n"

report_summary += "\n---\nBot automated by Jyoti"
send_email_alert(report_summary)
print("Filtered Active Report email par bhej di gayi hai!")
