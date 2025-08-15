import boto3
from botocore.client import Config
import os
from dotenv import load_dotenv  

load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")

s3_client = boto3.client(
  "s3",
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
  region_name=AWS_REGION,
  endpoint_url=f"https://{AWS_REGION}.amazonaws.com",
  config=Config(signature_version='s3v4')
)

def upload_file_to_s3(path: str, object_name: str) -> str:
	"""
	Upload a file to an S3 bucket.
	"""
	s3_client.upload_file(path, S3_BUCKET_NAME, object_name, ExtraArgs={'ContentType': 'application/pdf'})
	return object_name

def get_signed_url(object_name: str) -> str:
	"""
	Get a signed URL for an S3 object.
	"""

	signed_url = s3_client.generate_presigned_url(
		"get_object",
		Params={
			"Bucket": S3_BUCKET_NAME,
			"Key": object_name
		},
		ExpiresIn=3600,
	)
	print(f"Signed URL: {signed_url}")
	return signed_url