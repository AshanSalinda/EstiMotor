from fastapi import APIRouter, BackgroundTasks

from ..utils.logger import info, warn, err

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    """Return the favicon for the API."""	
    # return FileResponse("path/to/your/favicon.ico")
    pass


@router.post("/start")
async def start_scraping_task(background_tasks: BackgroundTasks):
    """Start a scraping task in the background."""
    try:
        # background_tasks.add_task(start_scraping)
        return {"status": "Scraping started!"}

    except Exception as e:
        err(f"Failed to start scraping: {e}")
        return {"status": "Failed to start scraping task!"}


@router.post("/stop")
async def stop_scraping_task():
    """Stop an ongoing scraping task."""
    try:
        # stop_scraping()
        return {"status": "Scraping stopped!"}

    except Exception as e:
        err(f"Failed to stop scraping: {e}")
        return {"status": "Failed to stop scraping task!"}

