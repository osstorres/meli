from fastapi import FastAPI, HTTPException
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def root():
    # For testing :)
    return {"message": "Hello World!"}


handler = Mangum(app)
