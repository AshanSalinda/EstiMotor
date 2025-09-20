from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.api.websocket import router as websocket_router, cancel_sender_task
from app.db.database import database
from app.steps.shared.reactor_thread import reactor_thread
from app.utils.scheduler import scheduler


@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    # On startup
    reactor_thread.start()
    scheduler.start()

    # Application is running
    yield

    # On shutdown
    await cancel_sender_task()
    database.close()
    reactor_thread.stop()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(websocket_router)
