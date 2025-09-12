import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schema.schema import VehicleFeatures, PricePrediction
from app.service.get_ads import ads
from app.service.model import model
from app.utils.logger import err

router = APIRouter()


@router.get("/favicon.ico")
async def favicon():
    """
    Return the favicon for the API.
    This is a placeholder endpoint and not implemented.
    """
    pass


@router.post(
    "/train",
    summary="Train Model",
    description="Start the model training process in the background. Returns evaluation metrics upon completion.",
    response_description="Model training result"
)
async def start_scraping_task() -> JSONResponse:
    try:
        loop = asyncio.get_running_loop()
        evaluation_metrics = await loop.run_in_executor(None, model.train)
        return JSONResponse(
            content={
                "message": "Model trained successfully.",
                "evaluation_metrics": evaluation_metrics
            },
            status_code=200
        )

    except Exception as e:
        err(f"Modal training failed: {e}")
        return JSONResponse(
            content={"message": "Modal training failed"},
            status_code=500
        )


@router.post(
    "/predict",
    response_model=PricePrediction,
    summary="Predict Vehicle Price",
    description="Provide vehicle details to get an estimated resale price.",
    response_description="Predicted vehicle value",
)
async def predict_vehicle_value(vehicle: VehicleFeatures):
    try:
        vehicle_dict = vehicle.model_dump()
        predicted_value = model.predict(vehicle_dict)
        similar_ads = ads
        return PricePrediction(
            message="Prediction successful.",
            predictedValue=predicted_value,
            similarAds=similar_ads
        )

    except Exception as e:
        err(f"Prediction failed: {e}")
        return JSONResponse(
            content={"message": "Prediction failed", "value": 0},
            status_code=500
        )
