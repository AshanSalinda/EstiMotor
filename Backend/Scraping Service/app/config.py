import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "EstiMotor Web Scraper Service"
    API_V1_STR: str = "/api/v1"

    # Database
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set in environment variables!")
    if not DATABASE_NAME:
        raise ValueError("DATABASE_NAME is not set in environment variables!")


settings = Settings()
