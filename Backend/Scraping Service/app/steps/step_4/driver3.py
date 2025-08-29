from datetime import datetime

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.db.repository.cleaned_vehicle_data_repository import cleaned_vehicles_data_repo
from app.steps.shared.base_step import Step
from app.utils.logger import info, warn


class Driver(Step):
    """Training pipeline for vehicle price prediction."""

    def __init__(self):
        super().__init__(step_name="Model Training")
        self.model_path = "vehicle_price_model.pkl"

    def run(self):
        """Run the model training process."""
        info("Fetching vehicles from DB...")
        vehicles = cleaned_vehicles_data_repo.get_all()

        if not vehicles:
            warn("No vehicles found in DB.")
            return

        df = pd.DataFrame(vehicles)

        # ------------------------------
        # Feature Engineering
        # ------------------------------
        current_year = datetime.now().year
        df["age"] = current_year - df["yom"].astype(int)

        # Avoid division by zero
        df["mileage_per_year"] = df.apply(
            lambda row: row["mileage"] / row["age"] if row["age"] > 0 else row["mileage"],
            axis=1
        )

        # ------------------------------
        # Features / Target
        # ------------------------------
        X = df[["make", "model", "engine_capacity", "mileage", "transmission",
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
        categorical = ["make", "model", "transmission", "fuel_type"]
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

        mae = mean_absolute_error(y_test_exp, y_pred_exp)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        r2 = r2_score(y_test_exp, y_pred_exp)

        info(f"Evaluation Results:")
        info(f"MAE:  {mae:.2f}")
        info(f"MAPE: {mape:.2f}%")
        info(f"R²:   {r2:.4f}")

        joblib.dump(model, self.model_path)
        info("Model training completed.")


Driver().run()