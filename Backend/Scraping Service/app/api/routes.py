from fastapi import APIRouter
from app.utils.logger import err
from app.steps.shared.steps_manager import StepsManager

router = APIRouter()


@router.get("/favicon.ico")
async def favicon():
    """Return the favicon for the API."""
    # return FileResponse("path/to/your/favicon.ico")
    pass


@router.post("/start")
async def start_scraping_task():
    """Start Model training process in the background."""

    try:
        StepsManager().start()
        return {"message": "Model training process started"}

    except Exception as e:
        err(f"Failed to start scraping: {e}")
        return {"message": "Failed to start Model training process"}


@router.post("/stop")
async def stop_scraping_task():
    """Stop an ongoing Model training process."""

    try:
        # await driver.stop_scraping()
        return {"message": "Model training process stopped"}

    except Exception as e:
        err(f"Failed to stop scraping: {e}")
        return {"message": "Failed to stop Model training process"}
