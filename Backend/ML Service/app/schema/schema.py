from pydantic import BaseModel, Field


class VehicleFeatures(BaseModel):
    make: str
    model: str
    year: int
    mileage: float
    fuel_type: str = Field(..., alias="fuelType")
    transmission: str
    engine_capacity: int = Field(..., alias="engineCapacity")

    class Config:
        json_schema_extra = {
            "example": {
                "make": "Toyota",
                "model": "Corolla",
                "year": 2019,
                "mileage": 35000,
                "fuelType": "Petrol",
                "transmission": "Automatic",
                "engineCapacity": 1800,
            }
        }
        validate_by_name = True


class PricePrediction(BaseModel):
    value: float = Field(..., description="Estimated resale price of the vehicle.")
    message: str = Field(..., description="Status message.")

    class Config:
        json_schema_extra = {
            "example": {"message": "Prediction successful.", "value": 15000.0}
        }
