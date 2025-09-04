import os, time
from rq import Connection, Worker
from redis import Redis

queue_name = "pbu-jobs"

if __name__ == "__main__":
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    redis = Redis.from_url(url)
    with Connection(redis):
        w = Worker([queue_name])
        w.work()
