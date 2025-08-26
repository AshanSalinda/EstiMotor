import joblib
import pandas as pd

# Load model
model = joblib.load("vehicle_price_model.pkl")

# Sample input
input_data = pd.DataFrame([{
    "make": "Toyota",
    "model": "Land Cruiser Prado",
    "yom": 2018,
    "transmission": "automatic",
    "fuel_type": "diesel",
    "engine_capacity": 3000,
    "mileage": 58000
}])

# Predict
predicted_price = model.predict(input_data)[0]
print(f"💰 Estimated Price: Rs. {predicted_price:,.2f}")
