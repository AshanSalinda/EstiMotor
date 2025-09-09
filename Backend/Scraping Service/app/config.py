import os
from dotenv import load_dotenv
from app.utils.logger import err

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

    if not MONGO_URI:
        err("MONGO_URI is not set in environment variables!")
        exit(1)
    if not DATABASE_NAME:
        err("DATABASE_NAME is not set in environment variables!")
        exit()

    # Modal API
    MODAL_TRAINING_URL: str = os.getenv("MODAL_TRAINING_URL")
    if not MODAL_TRAINING_URL:
        err("MODAL_TRAINING_URL is not set in environment variables!")
        exit(1)

    SCRAPING_BATCH_SIZE: int = int(os.getenv("SCRAPING_BATCH_SIZE", "100"))
    PROCESSING_BATCH_SIZE: int = int(os.getenv("PROCESSING_BATCH_SIZE", "1000"))


settings = Settings()
