import math

from app.data.parameters import *
from app.db.repository.cleaned_vehicle_data_repository import cleaned_vehicles_data_repo
from app.steps.shared.base_step import Step
from app.utils.logger import info, err

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error


class Driver(Step):
    """Class that manages the Model Training."""

    def __init__(self):
        super().__init__(step_name="Model Training")
        self.model_path = "vehicle_price_model.pkl"

    def run(self):
        """Start the model training process."""
        try:
            info("📦 Fetching cleaned data from MongoDB...")
            vehicles = cleaned_vehicles_data_repo.get_all()
            df = pd.DataFrame(vehicles)

            if df.empty:
                err("❌ No data found for model training.")
                return

            df.drop(columns=["_id"], inplace=True)

            # ---------- Log rows with any NaNs ----------
            missing_rows = df[df.isna().any(axis=1)]
            if not missing_rows.empty:
                info(f"⚠️ Found {len(missing_rows)} rows with missing values:")
                for i, row in missing_rows.iterrows():
                    info(f"  Row {i}: {row.to_dict()}")

            # Features and target
            X = df[[MAKE, MODEL, YOM, TRANSMISSION, FUEL_TYPE, ENGINE_CAPACITY, MILEAGE]]
            y = df[PRICE]

            categorical_cols = [MAKE, MODEL, TRANSMISSION, FUEL_TYPE]
            numerical_cols = [YOM, ENGINE_CAPACITY, MILEAGE]

            # ---------- Preprocessing Pipelines ----------
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median'))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', categorical_transformer, categorical_cols),
                    ('num', numerical_transformer, numerical_cols)
                ]
            )

            # ---------- Full Pipeline ----------
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', LinearRegression())
            ])

            # ---------- Train/Test Split ----------
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            info("🧠 Training model...")
            pipeline.fit(X_train, y_train)

            # ---------- Evaluation ----------
            y_pred = pipeline.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            # rmse = mean_squared_error(y_test, y_pred, squared=False)
            rmse = math.sqrt(mean_squared_error(y_test, y_pred))

            # ---------- Save Model ----------
            joblib.dump(pipeline, self.model_path)

            info(f"✅ Model trained and saved to {self.model_path}")
            info(f"📊 R² Score: {r2:.4f} | RMSE: {rmse:,.2f}")

        except Exception as e:
            err(f"❌ Model training failed. Error: {e}")


Driver().run()
