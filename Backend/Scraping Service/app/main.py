from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import database
from app.api.websocket import router as websocket_router
from app.web_scraper.driver import start_reactor, stop_reactor
from app.api.routes import router as api_router
from app.config import settings

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    database.connect()
    start_reactor()


@app.on_event("shutdown")
async def on_shutdown():
    database.close()
    stop_reactor()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(websocket_router)