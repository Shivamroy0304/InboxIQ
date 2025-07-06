from twilio.rest import Client
from telegram import Bot
import asyncio

TELEGRAM_TOKEN = ""
CHAT_ID = ""
bot = Bot(token=TELEGRAM_TOKEN)

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = "+1"
YOUR_PHONE_NUMBER = "+91"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def make_voice_call(summary):
    """Trigger a Twilio voice call with the summary."""
    message = f"You have an important email alert. Summary: {summary}"
    call = client.calls.create(
        twiml=f'<Response><Say>{message}</Say></Response>',
        to=YOUR_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER
    )
    print("📞 Call initiated with SID:", call.sid)

async def send_summary(summary):
    """Send summary via Telegram and trigger call."""
    await bot.send_message(chat_id=CHAT_ID, text=summary)
    make_voice_call(summary)
