from fastapi import APIRouter
router = APIRouter()

@router.get("/{job_id}")
async def get_job(job_id: str):
    # TODO: return job status + output url
    return {"id": job_id, "status": "processing"}
