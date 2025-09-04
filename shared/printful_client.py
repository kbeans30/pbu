"""Minimal Printful Mockup Generator client.

Docs: https://developers.printful.com/docs/#tag/Mockup-Generator
Flow:
  1) Create task: POST /mockup-generator/create-task/{variant_id}
  2) Poll task:  GET  /mockup-generator/task?task_key=...
  3) Download first image URL from result
"""
import os
import time
import requests

PRINTFUL_API_KEY = os.environ.get("PRINTFUL_API_KEY")
PRINTFUL_STORE_ID = os.environ.get("PRINTFUL_STORE_ID")

API_BASE = "https://api.printful.com"

class PrintfulError(Exception):
    pass

def _headers():
    if not PRINTFUL_API_KEY:
        raise PrintfulError("Missing PRINTFUL_API_KEY")
    return {"Authorization": f"Bearer {PRINTFUL_API_KEY}", "Content-Type": "application/json"}

def create_mockup_task(variant_id: int, printfile_url: str, placement: str = "front", background: str = "white") -> str:
    """Start a mockup task with a single print file on a given placement."""
    payload = {
        "variant_ids": [variant_id],
        "format": "png",
        "files": [
            {"placement": placement, "image_url": printfile_url}
        ],
        "product_options": {},
        "options": {"background": background}
    }
    r = requests.post(f"{API_BASE}/mockup-generator/create-task/{variant_id}", headers=_headers(), json=payload, timeout=30)
    if r.status_code >= 300:
        raise PrintfulError(f"Create task failed: {r.status_code} {r.text}")
    data = r.json()
    task_key = data.get("result", {}).get("task_key")
    if not task_key:
        raise PrintfulError(f"No task_key in response: {data}")
    return task_key

def poll_task(task_key: str, timeout_s: int = 60) -> dict:
    """Poll a task until done or timeout."""
    start = time.time()
    while time.time() - start < timeout_s:
        r = requests.get(f"{API_BASE}/mockup-generator/task", headers=_headers(), params={"task_key": task_key}, timeout=15)
        if r.status_code >= 300:
            raise PrintfulError(f"Task poll failed: {r.status_code} {r.text}")
        data = r.json()
        status = data.get("result", {}).get("status")
        if status == "completed":
            return data["result"]
        if status in ("failed", "canceled"):
            raise PrintfulError(f"Task {status}: {data}")
        time.sleep(2)
    raise PrintfulError("Mockup task timed out")

def first_mockup_png(task_result: dict) -> str:
    """Extract first mockup image URL from completed result."""
    mocks = task_result.get("mockups") or []
    if not mocks or not mocks[0].get("files"):
        raise PrintfulError("No mockup files in result")
    # Pick the first file's URL
    return mocks[0]["files"][0]["url"]
