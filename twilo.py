from twilio.rest import Client

client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

call = client.calls.create(
    twiml='<Response><Say>Hello Shivam, please check your importent email.</Say></Response>',
    to='+91',
    from_='+1'
)

print("Call initiated:", call.sid)
