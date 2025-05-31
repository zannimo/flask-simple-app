import json
import boto3
import os
from decimal import Decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Key 

# Set AWS region (hardcoded or from Lambda environment)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Set main table and GSI from environment variables
MOVIE_TABLE = os.environ.get("DYNAMODB_TABLE")
if not MOVIE_TABLE:
    raise ValueError("DYNAMODB_TABLE environment variable is not set.")

INDEX_NAME = os.environ.get("INDEX_NAME")
if not INDEX_NAME:
    raise ValueError("INDEX_NAME environment variable is not set.")

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(MOVIE_TABLE)


# Custom JSON encoder for Decimal types (used by DynamoDB)
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


# Utility for standardized error responses
def error_response(message, exception=None):
    if exception:
        print(f"Error: {message}: {exception}")
    else:
        print(f"Error: {message}")
    return {
        "statusCode": 500,
        "body": json.dumps({"message": message, "error": str(exception) if exception else "Unknown error"}, cls=JSONEncoder),
        "headers": {"Content-Type": "application/json"},
    }


# Handlers
def get_all_movies():
    try:
        response = table.scan()
        movies = response.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Movies retrieved successfully", "movies": movies}, cls=JSONEncoder),
            "headers": {"Content-Type": "application/json"},
        }
    except ClientError as e:
        return error_response("Failed to retrieve movies", e)


def get_movies_by_year(year):
    try:
        response = table.query(
            IndexName=INDEX_NAME,
            KeyConditionExpression=Key("year").eq(int(year))
        )
        movies = response.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Movies from year {year} retrieved successfully", "movies": movies}, cls=JSONEncoder),
            "headers": {"Content-Type": "application/json"},
        }
    except ClientError as e:
        return error_response(f"Failed to retrieve movies from year {year}", e)


def get_movie_summary(movie_id):
    try:
        response = table.get_item(Key={"id": movie_id})
        movie = response.get("Item")

        if not movie:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Movie not found"}),
                "headers": {"Content-Type": "application/json"},
            }

        summary = {
            "id": movie["id"],
            "title": movie["title"],
            "year": movie["year"],
            "summary": movie.get("summary", "No summary available"),
        }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Movie summary retrieved successfully", "movie": summary}, cls=JSONEncoder),
            "headers": {"Content-Type": "application/json"},
        }

    except ClientError as e:
        return error_response(f"Failed to retrieve movie summary for ID {movie_id}", e)


# Lambda entry point
STAGE = os.environ.get("STAGE", "dev")  # Fallback to "dev" if not set
def lambda_handler(event, context):
    print(f"Incoming event: {json.dumps(event)}")

    path = event.get("rawPath", "")
    path_params = event.get("pathParameters", {})

    if path.startswith(f"/{STAGE}/"):
        path = "/" + path[len(f"/{STAGE}/"):]

    print(f"Resolved path: {path}")
    print(f"Path parameters: {path_params}")

    if path == "/getmovies":
        return get_all_movies()

    elif path.startswith("/getmoviesbyyear/"):
        year = path_params.get("id")
        if not year:
            return {"statusCode": 400, "body": json.dumps({"message": "Year parameter is missing"}), "headers": {"Content-Type": "application/json"}}
        return get_movies_by_year(year)

    elif path.startswith("/getmoviesummary/"):
        movie_id = path_params.get("id")
        if not movie_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Movie ID is missing"}), "headers": {"Content-Type": "application/json"}}
        return get_movie_summary(movie_id)

    return {"statusCode": 404, "body": json.dumps({"message": "Route not found"}), "headers": {"Content-Type": "application/json"}}
