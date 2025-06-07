import boto3
import subprocess

AWS_REGION = "us-east-1"

# Helper function that runs a terraform output command and returns the result as a string
def get_output(name):
    return subprocess.check_output(["terraform", "-chdir=../terraform", "output", "-raw", name], text=True).strip()

# Use that function to dynamically fetch values from terraform
STATIC_S3_BUCKET = get_output("static_s3_bucket_name")

# AWS Clients
s3 = boto3.client("s3") 

# Upload index.html and error.html
s3.upload_file("../frontend/templates/index.html", STATIC_S3_BUCKET, "index.html", ExtraArgs={"ContentType": "text/html"})
s3.upload_file("../frontend/templates/error.html", STATIC_S3_BUCKET, "error.html", ExtraArgs={"ContentType": "text/html"})

# Upload JS and CSS under static/
s3.upload_file("../frontend/static/app.js", STATIC_S3_BUCKET, "static/app.js", ExtraArgs={"ContentType": "application/javascript"})
s3.upload_file("../frontend/static/style.css", STATIC_S3_BUCKET, "static/style.css", ExtraArgs={"ContentType": "text/css"})