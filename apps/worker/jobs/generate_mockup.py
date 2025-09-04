import io
import os
import requests
from shared.printful_client import create_mockup_task, poll_task, first_mockup_png
from shared.s3_utils import upload_bytes

# ENV you must set:
# - PRINTFUL_API_KEY
# - PRINTFUL_STORE_ID
# - PRINTFUL_VARIANT_ID (e.g., a varsity jacket variant)
# - PRINTFUL_CHEST_PATCH_URL (transparent PNG of Herbivore 'H' patch)
# - S3_BUCKET / S3_REGION / S3_ACCESS_KEY / S3_SECRET_KEY

def run(job_id: str, team: str = "herbivore") -> dict:
    """Generate a varsity jacket mockup (team color/patch), upload to S3, return URL."""
    variant_id = int(os.environ.get("PRINTFUL_VARIANT_ID", "0"))
    patch_url = os.environ.get("PRINTFUL_CHEST_PATCH_URL")
    if not (variant_id and patch_url):
        return {"job_id": job_id, "status": "error", "error": "Missing PRINTFUL_VARIANT_ID or PRINTFUL_CHEST_PATCH_URL"}

    # Create & poll Printful mockup task
    task_key = create_mockup_task(variant_id=variant_id, printfile_url=patch_url, placement="front", background="white")
    result = poll_task(task_key)
    mock_url = first_mockup_png(result)

    # Fetch PNG bytes
    png = requests.get(mock_url, timeout=30).content

    # Upload to S3 under /mockups/{job_id}.png
    key = f"mockups/{job_id}.png"
    url = upload_bytes(key, png, content_type="image/png", public=True)

    return {"job_id": job_id, "status": "done", "mockup_url": url, "provider_url": mock_url}
