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
    msg.subject = "🚨 Advanced Smart Stock Signals Report!"
    msg['From'] = sender_email
    msg['To'] = sender_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Advanced report email par bhej di gayi hai! 📧")
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

report_summary = "Smart Filtered Stock Signals (50 MA + RSI + Volume Spike):\n\n"
active_signals_count = 0

for symbol in symbols:
    try:
        stock_data = yf.download(symbol, period="90d", interval="1d", progress=False)
        if stock_data.empty or len(stock_data) < 60:
            continue
            
        close = stock_data['Close']
        volume = stock_data['Volume']
        
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
            
        # Volume Spike Check (Latest volume > 1.5x of 20-day average volume)
        avg_vol = volume.rolling(window=20).mean().iloc[-1]
        latest_vol = volume.iloc[-1]
        is_volume_spike = latest_vol > (1.5 * avg_vol)
        
        clean_name = symbol.replace(".NS", "")
        
        # Filter Logic: Price above 50MA & RSI > 50 for Buy; Price below 50MA & RSI < 50 for Sell
        if latest_price > ma_50 and rsi > 50:
            signal = f"🟢 BUY : {clean_name} | Price: {latest_price:.2f} | RSI: {rsi:.1f} | Vol Spike: {'Yes 🔥' if is_volume_spike else 'Normal'}\n"
            report_summary += signal
            active_signals_count += 1
        elif latest_price < ma_50 and rsi < 50:
            signal = f"🔴 SELL : {clean_name} | Price: {latest_price:.2f} | RSI: {rsi:.1f} | Vol Spike: {'Yes 🔥' if is_volume_spike else 'Normal'}\n"
            report_summary += signal
            active_signals_count += 1
            
    except Exception as e:
        continue

if active_signals_count == 0:
    report_summary += "Aaj koi strong active signal match nahi hua.\n"

report_summary += "\n---\nBot automated by Jyoti"
send_email_alert(report_summary)
print("Advanced scan aur email bhejne ka kaam poora ho gaya!")
