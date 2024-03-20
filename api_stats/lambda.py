from fastapi import FastAPI, HTTPException
import boto3
import os
from mangum import Mangum
from collections import Counter
from operator import itemgetter

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


@app.get("/status_code_most_common")
async def get_most_common_status_code():
    items = dynamodb_service.scan_table()
    status_codes = [item["response_code"]["N"] for item in items]
    status_code_counter = Counter(status_codes)
    most_common_status_code = status_code_counter.most_common(1)
    return {"most_common_status_code": most_common_status_code[0][0]}


@app.get("/path_most_common")
async def get_most_common_path():
    items = dynamodb_service.scan_table()
    paths = [item["path"]["S"] for item in items]
    path_counter = Counter(paths)
    most_common_path = path_counter.most_common(1)
    return {"most_common_path": most_common_path[0][0]}


@app.get("/cache_percentage")
async def get_cache_percentage():
    items = dynamodb_service.scan_table()
    total_requests = len(items)
    cached_requests = sum(
        bool(item.get("cached", {}).get("BOOL", False)) for item in items
    )

    if total_requests == 0:
        return {"error": "No se encontraron solicitudes en la tabla."}

    percentage_cached = round((cached_requests / total_requests) * 100, 2)
    percentage_not_cached = round(100 - percentage_cached, 2)

    return {
        "cached_percentage": percentage_cached,
        "not_cached_percentage": percentage_not_cached,
    }


@app.get("/stats")
async def get_stats():
    items = dynamodb_service.scan_table()
    return {"stats": items}


handler = Mangum(app)
