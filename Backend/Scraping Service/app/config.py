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

    # Modal Training
    MODAL_TRAINING_URL: str = os.getenv("MODAL_TRAINING_URL")
    if not MODAL_TRAINING_URL:
        err("MODAL_TRAINING_URL is not set in environment variables!")
        exit(1)

    SCRAPING_BATCH_SIZE: int = int(os.getenv("SCRAPING_BATCH_SIZE", "100"))
    PROCESSING_BATCH_SIZE: int = int(os.getenv("PROCESSING_BATCH_SIZE", "1000"))

    # Email
    EMAIL_SENDER_ADDRESS: str = os.getenv("EMAIL_SENDER_ADDRESS")
    EMAIL_SENDER_PASSWORD: str = os.getenv("EMAIL_SENDER_PASSWORD")

    if not EMAIL_SENDER_ADDRESS:
        err("EMAIL_SENDER_ADDRESS is not set in environment variables!")
        exit(1)
    if not EMAIL_SENDER_PASSWORD:
        err("EMAIL_SENDER_PASSWORD is not set in environment variables!")
        exit(1)


settings = Settings()
