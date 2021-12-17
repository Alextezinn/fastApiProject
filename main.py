from fastapi import FastAPI
import uvicorn

from fastApiProject.db import database
from routes import routes


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(routes)

if __name__ == "__main__":
    uvicorn.run("main:app")
