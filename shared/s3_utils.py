import os
import boto3
from botocore.client import Config

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_REGION = os.environ.get("S3_REGION")
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")

def _client():
    return boto3.client(
        "s3",
        region_name=S3_REGION,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )

def upload_bytes(key: str, data: bytes, content_type: str = "image/png", public: bool = True) -> str:
    s3 = _client()
    extra = {"ContentType": content_type}
    if public:
        extra["ACL"] = "public-read"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data, **extra)
    # Public URL (adjust if using a CDN/custom domain)
    if S3_REGION and S3_REGION.startswith("us-east-1"):
        endpoint = f"https://{S3_BUCKET}.s3.amazonaws.com"
    else:
        endpoint = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com"
    return f"{endpoint}/{key}"
