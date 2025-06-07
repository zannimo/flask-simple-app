import boto3
import os
import subprocess

AWS_REGION = "us-east-1"

# Helper function that runs a terraform output command and returns the result as a string
def get_output(name):
    return subprocess.check_output(["terraform", "-chdir=../terraform", "output", "-raw", name], text=True).strip()

# Use that function to dynamically fetch values from terraform
STATIC_S3_BUCKET = get_output("static_s3_bucket_name")

# AWS Clients
s3_client = boto3.client("s3") 

# ... 


