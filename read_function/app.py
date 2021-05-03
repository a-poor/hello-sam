import os
import json
import boto3
from io import StringIO, BytesIO
from datetime import datetime


def lambda_handler(event, context):
    try:
        bucket = os.environ["BUCKET_NAME"]
    except:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": False,
                "message": "Couldn't find BUCKET_NAME environment variable."
            })
        }

    try:
        s3 = boto3.client("s3")
    except Exception as e:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": False,
                "message": "Error connecting to s3: " + str(e)
            })
        }

    try:
        results = s3.list_objects_v2(Bucket=bucket)
    except Exception as e:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": False,
                "message": f"Error reading from s3 bucket {bucket}: " + str(e)
            })
        }

    keys = [r["Key"] for r in results.get("Contents",[])]
    data = [json.load(s3.get_object(Bucket=bucket,Key=k)["Body"]) for k in keys]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": True,
            "message": None,
            "contents": data
        })
    }
