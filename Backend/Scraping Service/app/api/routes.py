from fastapi import APIRouter
from fastapi import HTTPException
from ..web_scraper.driver import start_scraping, stop_scraping
from ..utils.logger import info, warn, err

router = APIRouter()


@router.get("/favicon.ico")
async def favicon():
    """Return the favicon for the API."""
    # return FileResponse("path/to/your/favicon.ico")
    pass



@router.get("/start")
async def start_scraping_task():
    """Start a scraping task in the background."""

    try:
        start_scraping()
        return {"status": "Scraping started!"}

    except Exception as e:
        err(f"Failed to start scraping: {e}")
        return {"status": "Failed to start scraping task!"}
    except HTTPException as e:
        err(f"Failed to start scraping: {e}")
        return {"status": "Failed to start scraping task!"}
    except RuntimeError as e:
        err(f"Failed to start scraping: {e}")
        return {"status": "Failed to start scraping task!"}



@router.get("/stop")
async def stop_scraping_task():
    """Stop an ongoing scraping task."""
   
    try:
        stop_scraping()
        return {"status": "Scraping stopped!"}

    except Exception as e:
        err(f"Failed to stop scraping: {e}")
        return {"status": "Failed to stop scraping task!"}
