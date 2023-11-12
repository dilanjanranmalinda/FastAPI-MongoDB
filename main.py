from fastapi import FastAPI
import uvicorn
from database.connection import connect_db
from routes.products import products_api
from routes.tasks import tasks_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(products_api)

app.include_router(tasks_api)


@app.on_event("startup")
async def startup_event():
    connect = connect_db()
    print(connect)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
