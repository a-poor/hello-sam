import os
import json
import boto3
from io import BytesIO
from datetime import datetime


def lambda_handler(event, context):
    bucket = os.environ["BUCKET_NAME"]

    d = datetime.now()
    fn = d.strftime("%y%m%d-%H%M%S.json")

    data = json.dumps({
        "timestamp": str(d)
    })

    f = BytesIO(data.encode())

    s3 = boto3.client("s3")
    s3.upload_fileobj(f, bucket, fn)
