import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_sms(phone, message):
    api_key = os.getenv("KAVENEGAR_API_KEY")
    api_url = os.getenv("KAVENEGAR_API_URL")
    sender = os.getenv("KAVENEGAR_API_SENDER_NUMBER")

    if not api_key or not api_url:
        raise Exception("Kavenegar API credentials are missing in .env")

    payload = {
        "sender":sender,
        "receptor": phone,
        "message": message,
    }

    response = requests.post(f'{api_url}/{api_key}/sms/send.json', data=payload)
    response.raise_for_status()  # Raises an error for HTTP 4xx/5xx
    return response.json()
