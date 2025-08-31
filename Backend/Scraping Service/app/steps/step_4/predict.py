from datetime import datetime

import joblib
import numpy as np
import pandas as pd

# Load model
model = joblib.load("vehicle_price_model.pkl")

random_forest = True

input_data = {
  "_id": {
    "$oid": "68b195b0e724cb9007bad345"
  },
  "url": "https://patpat.lk/en/ad/vehicle/toyota-land-cruiser-prado-2002-86885",
  "price": 15200000,
  "mileage": 165000,
  "yom": 2002,
  "engine_capacity": 2700,
  "make": "Toyota",
  "transmission": "automatic",
  "fuel_type": "petrol",
  "model": "Land Cruiser Prado"
}

#------------------------------------------

input_data.pop("_id", None)
input_data.pop("index", None)
input_data.pop("url", None)
input_data.pop("price", None)

if random_forest:
    current_year = datetime.now().year
    input_data["age"] = current_year - input_data.pop("yom")
    input_data["mileage_per_year"] = input_data["mileage"] / input_data["age"]

input_pd = pd.DataFrame([input_data])

# Predict
if random_forest:
    predicted_price = np.expm1(model.predict(input_pd)[0])
else:
    predicted_price = model.predict(input_pd)[0]

print(f"💰 Estimated Price: Rs. {predicted_price:,.2f}")
