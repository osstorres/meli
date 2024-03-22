import boto3
import os
from datetime import datetime
import json
import uuid

class DynamoDBService:
    def __init__(self, endpoint_url=None):
        if endpoint_url:
            self.client = boto3.client("dynamodb", endpoint_url=endpoint_url)
        else:
            self.client = boto3.client("dynamodb")

    def put_item(self, table_name, item):
        self.client.put_item(TableName=table_name, Item=item)


class MessageProcessor:
    def __init__(self, dynamodb_service, dynamodb_table_name):
        self.dynamodb_service = dynamodb_service
        self.dynamodb_table_name = dynamodb_table_name

    def process_messages(self, event):
        """
        The process_messages function is the main function of this Lambda.
        It takes in an event, which is a list of SQS messages. It then
        iterates through each message and parses it into a JSON object,
        which it then uses to create an item for DynamoDB. The item contains
        all the information from the SQS message as well as a date_key
        attribute that stores when the request was made.

        :param event: Get the records from the sqs queue
        :return: None
        """
        for record in event["Records"]:
            body = json.loads(record["body"])

            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_id = str(uuid.uuid4())
            item = {
                "id": {"S": unique_id},
                "date_key": {"S": current_datetime},
                "query_params": {"S": json.dumps(body.get("query_params", {}))},
                "cached": {"BOOL": body.get("cached", False)},
                "path": {"S": body.get("path", "")},
                "ip_address": {"S": body.get("ip_address", "")},
                "method": {"S": body.get("method", "")},
                "response_code": {"N": str(body.get("response_code", 0))},
                "headers": {
                    "M": {
                        key: {"S": value}
                        for key, value in body.get("headers", {}).items()
                    }
                },
            }

            self.dynamodb_service.put_item(self.dynamodb_table_name, item)


def handler(event, context):
    print(f"MESSAGE {event}")
    dynamodb_service = DynamoDBService(endpoint_url=os.environ.get("DYNAMODB_ENDPOINT"))
    message_processor = MessageProcessor(
        dynamodb_service, os.environ.get("DYNAMODB_TABLE_NAME")
    )
    message_processor.process_messages(event)
    print("======")
    return {"statusCode": 200, "body": "OK"}
