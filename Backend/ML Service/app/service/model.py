import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.db.vehicle_data_repository import vehicle_data_repo
from app.utils.logger import info, warn


class Model:
    def __init__(self):
        self.model_path = "./app/service/vehicle_price_model.pkl"
        self.is_training = False
        self.model = None
        try:
            self._load_model()
        except Exception as e:
            warn(e)


    def _load_model(self):
        import joblib
        try:
            info(f"Loading model from {self.model_path}")
            self.model = joblib.load(self.model_path)
        except FileNotFoundError:
            raise Exception(f"Model not found at {self.model_path}")


    def predict(self, vehicle_data: dict):
        """Predict vehicle price."""

        if self.model is None:
            self._load_model()

        input_vehicle = vehicle_data.copy()
        current_year = datetime.now().year
        input_vehicle["age"] = current_year - input_vehicle.pop("year")
        input_vehicle["mileage_per_year"] = (
            input_vehicle["mileage"] / input_vehicle["age"]
            if not input_vehicle["age"] == 0 else 0
        )

        input_pd = pd.DataFrame([input_vehicle])

        # Predict
        predicted_price = np.expm1(self.model.predict(input_pd)[0])

        return predicted_price


    def train(self):
        """Train the model."""
        if self.is_training:
            raise Exception("Model training is already in progress.")

        try:
            info("Starting model training process...")

            self.is_training = True

            info("Fetching vehicles from DB...")
            vehicles = vehicle_data_repo.get_all()

            if not vehicles:
                raise Exception("No vehicle data available in DB.")

            df = pd.DataFrame(vehicles)

            # ------------------------------
            # Feature Engineering
            # ------------------------------
            current_year = datetime.now().year
            df["age"] = current_year - df["year"].astype(int)

            # Avoid division by zero
            df["mileage_per_year"] = df.apply(
                lambda row: row["mileage"] / row["age"] if row["age"] > 0 else row["mileage"],
                axis=1
            )

            # ------------------------------
            # Features / Target
            # ------------------------------
            X = df[["make", "model", "category", "engine_capacity", "mileage", "transmission",
                    "fuel_type", "age", "mileage_per_year"]]
            y = df["price"]

            # Apply log transformation to target
            y = np.log1p(y)

            # ------------------------------
            # Train/Test Split
            # ------------------------------
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # ------------------------------
            # Preprocessor
            # ------------------------------
            categorical = ["make", "model", "category", "transmission", "fuel_type"]
            numeric = ["engine_capacity", "mileage", "age", "mileage_per_year"]

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), numeric),
                    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
                ]
            )

            # ------------------------------
            # Model (Random Forest)
            # ------------------------------
            model = Pipeline(steps=[
                ("preprocessor", preprocessor),
                ("regressor", RandomForestRegressor(
                    n_estimators=200,
                    max_depth=None,
                    random_state=42,
                    n_jobs=-1
                )),
            ])

            info("Training model (RandomForest with log(price))...")
            model.fit(X_train, y_train)

            # ------------------------------
            # Evaluation
            # ------------------------------
            y_pred = model.predict(X_test)

            # Transform back from log(price)
            y_test_exp = np.expm1(y_test)
            y_pred_exp = np.expm1(y_pred)

            # Evaluation Metrics
            mae = mean_absolute_error(y_test_exp, y_pred_exp)
            mape = np.mean(np.abs((y_test_exp - y_pred_exp) / y_test_exp)) * 100
            r2 = r2_score(y_test_exp, y_pred_exp)

            # Save the model
            joblib.dump(model, self.model_path)

            self._load_model()

            info(f"Evaluation Results:")
            info(f"MAE:  {mae:.2f}")
            info(f"MAPE: {mape:.2f}%")
            info(f"R²:   {r2:.4f}")
            info("Model training completed.")

            return {
                "MAE": f"{mae:.2f}",
                "MAPE": f"{mape:.2f}%",
                "R2": f"{r2:.4f}"
            }

        finally:
            self.is_training = False


model = Model()
