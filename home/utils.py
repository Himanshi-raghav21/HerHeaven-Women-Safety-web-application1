from twilio.rest import Client
from decouple import config


# Load from .env
TWILIO_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH = config('TWILIO_AUTH_TOKEN')
TWILIO_SMS_NUMBER = config('TWILIO_PHONE_NUMBER')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(to, body):
    message = client.messages.create(
        body=body,
        from_=TWILIO_SMS_NUMBER,
        to=to   # Make sure it's E.164 format like +91xxxxxx
    )
    return message.sid

def send_whatsapp(to, body):
    message = client.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{to}"
    )
    return message.sid
