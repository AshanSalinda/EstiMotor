from fastapi import APIRouter
from app.utils.logger import err
from app.steps.shared.steps_manager import steps_manager

router = APIRouter()


@router.get("/favicon.ico")
async def favicon():
    """Return the favicon for the API."""
    # return FileResponse("path/to/your/favicon.ico")
    pass


@router.post("/start")
async def start_scraping_task():
    """Start a scraping task in the background."""

    try:
        steps_manager.start()
        return {"status": "Scraping started!"}

    except Exception as e:
        err(f"Failed to start scraping: {e}")
        return {"status": "Failed to start scraping task!"}


@router.post("/stop")
async def stop_scraping_task():
    """Stop an ongoing scraping task."""

    try:
        # await driver.stop_scraping()
        return {"status": "Scraping stopped!"}

    except Exception as e:
        err(f"Failed to stop scraping: {e}")
        return {"status": "Failed to stop scraping task!"}
