import json
import os
from pathlib import PurePosixPath
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import boto3


TEMPOOK_DOWNLOAD_URL = "https://storage.tempook.com/tokstorage/download_post/"
s3 = boto3.client("s3")


def download_to_s3(path):
    token = os.environ["TEMPOOK_TOKEN"]
    bucket = os.environ["TEMPOOK_DOWNLOAD_BUCKET"]
    prefix = os.environ["TEMPOOK_S3_PREFIX"].strip("/")
    filename = PurePosixPath(path).name

    if not token:
        raise ValueError("The TEMPOOK_TOKEN environment variable must not be empty.")
    if not filename:
        raise ValueError("The TempoOK path must include a filename.")

    form_data = urlencode({"t": token, "p": path}).encode("utf-8")
    request = Request(
        TEMPOOK_DOWNLOAD_URL,
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        content = response.read()
        content_type = response.headers.get_content_type()

    key = f"{prefix}/{filename}" if prefix else filename
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=content,
        ContentType=content_type,
    )

    return {"bucket": bucket, "key": key, "size": len(content)}


def handler(event, context):
    if not isinstance(event, dict):
        raise ValueError("The invocation event must be an object.")

    path = event.get("path")
    if not isinstance(path, str) or not path.strip():
        raise ValueError("The invocation event must include a non-empty 'path'.")

    result = download_to_s3(path)
    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
