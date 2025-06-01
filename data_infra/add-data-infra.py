import boto3
import csv
import os
import uuid
import subprocess

AWS_REGION = "us-east-1"

# Helper function that runs a terraform output command and returns the result as a string
def get_output(name):
    return subprocess.check_output(["terraform", "-chdir=../terraform", "output", "-raw", name], text=True).strip()

# Use that function to dynamically fetch values from terraform
BUCKET_NAME = get_output("s3_bucket_name")
DYNAMODB_TABLE = get_output("dynamodb_table_name")


# AWS Clients
s3_client = boto3.client("s3") 
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

# Function to upload file to S3 and return its public URL
def upload_to_s3(local_path): # the argument for "local-path" will be the path in the csv file under field "cover_file" (eg, 'images/inception.jpg')
    filename = local_path  
    s3_client.upload_file(local_path, BUCKET_NAME, filename) 
    return f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"

# Read and process CSV file
csv_file = "movies.csv"

with open(csv_file, mode="r", encoding="utf-8") as file: # Opens the CSV file for reading
    reader = csv.DictReader(file) # Reads the file and creates a dictionary for each row. "reader" becomes an iterator over those dictionaries
    
    for row in reader: # Loops through the dictionaries, processing each row
        cover_file = row["cover_file"]  # Example: 'images/inception.jpg'
        
        # Ensure the image file exists before uploading
        if not os.path.exists(cover_file): # The name of the images in the CSV file is the the actual system path they are located under
            print(f"Error: File {cover_file} not found!")
            continue
        
        # Upload image and get the S3 URL, calling the function earlier defined
        s3_url = upload_to_s3(cover_file)
        
        # Insert into DynamoDB (excluding 'cover_file' and adding 'cover_url')
        item = {
            "id": str(uuid.uuid4()),
            "title": row["title"],
            "year": int(row["year"]),
            "genre": row["genre"],
            "cover_url": s3_url,  # Replacing local path with S3 URL
        }

        table.put_item(Item=item)
        print(f"Uploaded {row['title']} successfully!")
