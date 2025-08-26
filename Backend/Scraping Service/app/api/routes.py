from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.logger import err
from app.steps.shared.steps_manager import stepsManager

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
        if stepsManager.is_running:
            return JSONResponse(
                content={"message": "Model training process is already running."},
                status_code=409
            )

        stepsManager.start()
        return JSONResponse(
            content={"message": "Model training process started"},
            status_code=200
        )

    except Exception as e:
        err(f"Failed to start scraping: {e}")
        return JSONResponse(
            content={"message": "Failed to start Model training process"},
            status_code=500
        )


@router.post("/stop")
async def stop_scraping_task():
    """Stop an ongoing Model training process."""

    try:
        # await driver.stop_scraping()
        return JSONResponse(
            content={"message": "Model training process stopped"},
            status_code=200
        )

    except Exception as e:
        err(f"Failed to stop scraping: {e}")
        return JSONResponse(
            content={"message": "Failed to stop Model training process"},
            status_code=500
        )
