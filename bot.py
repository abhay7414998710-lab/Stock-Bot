import requests

token = "8816713797:AAEMNKiCD1H0IPVIrpwzgNzgV_shPm7h9Pg"
chat_id = "6150123285"
url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": "Hello Jyoti! Test message from your stock bot 🚀"
}

response = requests.post(url, json=payload)
print("TEST RESPONSE:", response.text)
