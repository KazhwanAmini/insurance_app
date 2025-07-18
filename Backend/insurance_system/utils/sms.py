import os
import requests
from dotenv import load_dotenv
from insurance.models import SMSLog

load_dotenv()

import jdatetime

# Example: Convert Gregorian date to Jalali
def convert_to_persian(gregorian_date):
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
    return jalali_date.strftime('%Y/%m/%d')  # Format: 1403/04/27

def send_sms(phone, message, company):
    api_key = os.getenv("KAVENEGAR_API_KEY")
    api_url = os.getenv("KAVENEGAR_API_URL")
    sender = os.getenv("KAVENEGAR_API_SENDER_NUMBER")

    if not api_key or not api_url:
        raise Exception("Kavenegar API credentials are missing in .env")

    payload = {
        "sender": sender,
        "receptor": phone,
        "message": message,
    }

    # ✅ Send SMS first
    response = requests.post(f'{api_url}/{api_key}/sms/send.json', data=payload)
    response.raise_for_status()  # Raises an error if HTTP 4xx/5xx
    result = response.json()

    # ✅ Only deduct credit and log if success
    if company:
        if company.sms_credit >= 200:
            company.sms_credit -= 200
            company.save()
            SMSLog.objects.create(company=company, recipient=phone, message=message)
        else:
            raise Exception("Insufficient SMS credit")

    return result
