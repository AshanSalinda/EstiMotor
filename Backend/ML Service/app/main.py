from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import database
from app.api.routes import router

app = FastAPI(
    title="EstiMotor ML Service API",
    description="API for training and predicting vehicle resale prices using machine learning. Provide vehicle details to get an estimated resale price.",
    version="1.0.0"
)

@app.on_event("shutdown")
async def on_shutdown():
    database.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
