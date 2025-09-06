from fastapi import APIRouter, Request
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

@router.post("/sms")
async def sms_webhook(request: Request):
    # Minimal echo to verify wiring
    form = dict((await request.form()).items())
    body = form.get("Body", "")
    resp = MessagingResponse()
    resp.message(f"PBU Garvey here. You said: {body}")
    return str(resp)
