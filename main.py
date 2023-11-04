import logging
from fastapi import FastAPI
import uvicorn
from database.connection import connect_db
from logger.task_logger import request_logging_middleware
from routes.products import products_api
from routes.tasks import tasks_api

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,  # Set the log level to INFO for request logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

app.middleware('http')(request_logging_middleware)

app.include_router(products_api)

app.include_router(tasks_api)

@app.on_event("startup")
async def startup_event():
    connect = connect_db()
    print(connect)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
