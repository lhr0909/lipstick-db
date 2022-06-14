import os
import boto3

s3_client = boto3.client(
  's3',
  endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
  aws_access_key_id=os.environ.get('S3_ACCESS_KEY_ID'),
  aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY'),
  region_name=os.environ.get('S3_REGION'),
)

s3_resource = boto3.resource(
  's3',
  endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
  aws_access_key_id=os.environ.get('S3_ACCESS_KEY_ID'),
  aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY'),
  region_name=os.environ.get('S3_REGION'),
)
