import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = None
if account_sid and auth_token:
    client = Client(account_sid, auth_token)


def send_sms(to_number, message):
    """Send SMS using Twilio"""
    if not client:
        print("Twilio not configured")
        return {"success": False, "error": "Twilio not configured"}

    try:
        msg = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to_number
        )
        return {"success": True, "sid": msg.sid}
    except Exception as e:
        print("SMS Error:", str(e))
        return {"success": False, "error": str(e)}


def make_call(to_number, message):
    """Make a phone call and speak the message using Twilio"""
    if not client:
        print("Twilio not configured")
        return {"success": False, "error": "Twilio not configured"}

    try:
        call = client.calls.create(
            twiml=f'<Response><Say>{message}</Say></Response>',
            from_=twilio_number,
            to=to_number
        )
        return {"success": True, "sid": call.sid}
    except Exception as e:
        print("Call Error:", str(e))
        return {"success": False, "error": str(e)}