import os
from redis import Redis
from rq import Queue

QUEUE_NAME = "pbu-jobs"
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

def get_queue():
    return Queue(QUEUE_NAME, connection=Redis.from_url(REDIS_URL))

def enqueue_mockup(job_id: str, team: str = "herbivore"):
    q = get_queue()
    # Import string path to avoid heavy imports at module load
    return q.enqueue("apps.worker.jobs.generate_mockup.run", job_id, team, job_id=job_id)
