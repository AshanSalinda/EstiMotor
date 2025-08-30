from app.data.parameters import *
from app.db.repository.cleaned_vehicle_data_repository import cleaned_vehicles_data_repo
from app.steps.shared.base_step import Step
from app.utils.logger import info, err

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
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

            # --- 2. Define Features & Target ---
            target = PRICE
            features = [MAKE, MODEL, YOM, TRANSMISSION, FUEL_TYPE, ENGINE_CAPACITY, MILEAGE]

            x = df[features]
            y = df[target]

            # --- 3. Split Data ---
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            # --- 4. Define Preprocessing ---
            numeric_features = [YOM, MILEAGE, ENGINE_CAPACITY]
            categorical_features = [MAKE, MODEL, TRANSMISSION, FUEL_TYPE]

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), numeric_features),
                    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
                ]
            )

            # --- 5. Build Pipeline (NO Imputer here) ---
            model = Pipeline(steps=[
                ("preprocessor", preprocessor),
                ("regressor", LinearRegression())  # can replace with RandomForestRegressor, XGB, etc.
            ])

            # --- 6. Train Model ---
            info("🧠 Training model...")
            model.fit(x_train, y_train)

            # --- 7. Evaluate ---
            y_pred = model.predict(x_test)
            r2 = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            info(f"📊 R² Score: {r2:.4f} | MSE: {mse:,.2f}")

            # --- 8. Save Trained Model ---
            joblib.dump(model, self.model_path)
            info(f"✅ Model saved as {self.model_path}")

        except Exception as e:
            err(f"❌ Model training failed. Error: {e}")


Driver().run()
