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
    predictedValue: float
    similarAds: list
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Prediction successful.",
                "predictedValue": 15000.0,
                "similarAds": [
                        {
                            "image": 'https://example.lk/uploads/images/ad-10377793.jpg',
                            "title": 'Example Vehicle Title',
                            "year": 2020,
                            "mileage": 0,
                            "source": 'Example.lk',
                            "price": 0,
                            "url": 'https://example.lk/vehicles/ad-10377793'
                        }
                ]
            }
        }
