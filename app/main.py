from fastapi import FastAPI
from .routers.task import router as task_router
from .db import init_db

app = FastAPI()

app.include_router(task_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await init_db()
