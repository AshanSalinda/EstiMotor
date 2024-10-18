from fastapi import APIRouter, BackgroundTasks
from ..tasks.background import start_scraping_task, stop_scraping_task
from ..utils.logger import info, warn, err

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    """Return the favicon for the API."""	
    # return FileResponse("path/to/your/favicon.ico")
    pass


@router.get("/start")
async def start_scraping(background_tasks: BackgroundTasks):
    """Start a scraping task in the background."""
    try:
        start_scraping_task.delay()
        return {"status": "Scraping started!"}

    except Exception as e:
        err(f"Failed to start scraping: {e}")
        return {"status": "Failed to start scraping task!"}


@router.get("/stop")
async def stop_scraping():
    """Stop an ongoing scraping task."""
    try:
        stop_scraping_task()
        return {"status": "Scraping stopped!"}

    except Exception as e:
        err(f"Failed to stop scraping: {e}")
        return {"status": "Failed to stop scraping task!"}

