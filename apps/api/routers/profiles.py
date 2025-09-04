import uuid
from fastapi import APIRouter, UploadFile, File
from ..worker_queue import enqueue_mockup

router = APIRouter()

@router.post("/photo")
async def upload_photo(file: UploadFile = File(...)):
    # TODO: actually persist the file to storage; for MVP we just enqueue a mockup job
    job_id = uuid.uuid4().hex
    enqueue_mockup(job_id, team="herbivore")
    return {"status": "queued", "job_id": job_id}
