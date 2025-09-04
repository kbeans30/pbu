import os
from fastapi import FastAPI
from routers import sms, profiles, mockups, goals

app = FastAPI(title="PBU API")

app.include_router(sms.router, prefix="/webhooks/twilio")
app.include_router(profiles.router, prefix="/api/profile")
app.include_router(mockups.router, prefix="/api/mockups")
app.include_router(goals.router, prefix="/api/goals")

@app.get("/healthz")
def healthz():
  return {"ok": True}
