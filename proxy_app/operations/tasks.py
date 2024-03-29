from celery import shared_task
import json
import boto3
import os
from django.conf import settings
import logging


SQS_ENDPOINT = os.environ.get("SQS_ENDPOINT")
logger = logging.getLogger("django")


@shared_task()
def send_metadata_to_sqs(
    ip_address: str,
    method: str,
    path: str,
    query_params: dict,
    headers: dict,
    cached: bool,
    response_code: int,
):
    sqs_endpoint = os.environ.get("SQS_ENDPOINT")
    sqs = boto3.client("sqs", endpoint_url=sqs_endpoint)
    queue_url = os.environ.get("SQS_QUEUE_URL")
    # Metadata for the request
    metadata = {
        "ip_address": ip_address,
        "method": method,
        "path": path,
        "query_params": query_params,
        "headers": headers,
        "cached": cached,
        "response_code": response_code,
    }

    # Send metadata to SQS
    allowed_dynamodb = any(word in settings.CACHED_PATHS for word in path.split("/"))
    if allowed_dynamodb:
        logger.info(f"==== Dynamodb {path}")
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(metadata))
