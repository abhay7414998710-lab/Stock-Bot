import os
import requests

token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": "Hello Jyoti! Test message from your stock bot 🚀"
}

response = requests.post(url, json=payload)
print("TEST RESPONSE:", response.text)
