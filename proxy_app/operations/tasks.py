from celery import shared_task
import os


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
   pass
