from fastapi import FastAPI, HTTPException
import boto3
import os
from mangum import Mangum

app = FastAPI()


class DynamoDBService:
    def __init__(self, endpoint_url: str, table_name: str):
        """
        The __init__ function is called when the class is instantiated. It
        sets up the DynamoDB client and table name for use in other functions.

        :param endpoint_url: str: Specify the endpoint url for the dynamodb client
        :param table_name: str: Set the table name
        :return: None
        """
        if endpoint_url:
            self.client = boto3.client("dynamodb", endpoint_url=endpoint_url)
        else:
            self.client = boto3.client("dynamodb")
        self.table_name = table_name

    def scan_table(self):
        """
        The scan_table function scans the table and returns all
        items in the table.
        :return: A list of all items in the table.
        """
        response = self.client.scan(TableName=self.table_name)
        return response.get("Items", [])


dynamodb_service = DynamoDBService(
    endpoint_url=os.environ.get("DYNAMODB_ENDPOINT"),
    table_name=os.environ.get("DYNAMODB_TABLE_NAME"),
)


@app.get("/")
async def root():
    # For testing :)
    return {"message": "Hello World!"}


@app.get("/stats")
async def get_stats():
    items = dynamodb_service.scan_table()
    return {"stats": items}


handler = Mangum(app)
