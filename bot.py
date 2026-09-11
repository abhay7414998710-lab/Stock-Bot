import os
import smtplib
from email.message import EmailMessage
import yfinance as yf

def send_email_alert(report_text):
    sender_email = "abhay7414998710@gmail.com"
    app_password = os.environ.get("MAIL_PASS")
    
    msg = EmailMessage()
    msg.set_content(report_text)
    msg.subject = "🚨 Real-Time Top NSE Stocks Daily Report!"
    msg['From'] = sender_email
    msg['To'] = sender_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Real-time report successfully email par bhej di gayi hai! 📧")
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

report_summary = "Aaj ka Real-Time Top Stocks Scan Result:\n\n"
print("... Live market data fetch ho raha hai...\n")

for symbol in symbols:
    try:
        stock_data = yf.download(symbol, period="70d", interval="1d", progress=False)
        if stock_data.empty:
            continue
            
        close_prices = stock_data['Close']
        if hasattr(close_prices, "iloc"):
            latest_price = float(close_prices.iloc[-1])
            ma_50 = float(close_prices.rolling(window=50).mean().iloc[-1])
        else:
            continue
            
        clean_name = symbol.replace(".NS", "")
        if latest_price > ma_50:
            signal = f"🟢 BUY : {clean_name} | Price: {latest_price:.2f} | 50 MA: {ma_50:.2f}\n"
        else:
            signal = f"🔴 SELL : {clean_name} | Price: {latest_price:.2f} | 50 MA: {ma_50:.2f}\n"
            
        print(signal)
        report_summary += signal
    except Exception as e:
        print(f"⚠️ {symbol} ka data fetch karne mein error aaya.")

report_summary += "\n---\nBot automated by Jyoti"
send_email_alert(report_summary)
print("\nReal-time scan aur email ka kaam poora ho gaya! 📊📧")
