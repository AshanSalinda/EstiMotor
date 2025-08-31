import pandas as pd
from datetime import datetime
from app.utils.logger import warn


def impute_missing_fields(cleaned_vehicles: list, imputation_stats: dict):
    median_mileage_by_yom = imputation_stats.get("median_mileage_by_yom", {})
    mode_engine_capacity_by_make = imputation_stats.get("mode_engine_capacity_by_make", {})
    mode_transmission_by_make = imputation_stats.get("mode_transmission_by_make", {})
    current_year = datetime.now().year

    df = pd.DataFrame(cleaned_vehicles)

    def fill_mileage(row):
        if pd.isna(row['mileage']):
            yom = row.get('yom')
            imputation = 0 if yom == current_year else median_mileage_by_yom.get(str(yom), None)
            if imputation is not None:
                warn(f"Updating mileage '{row['mileage']}' to {imputation}: {row['url']}")
            return imputation
        return row['mileage']

    def fill_engine_capacity(row):
        if pd.isna(row['engine_capacity']):
            make = row.get('make', '')
            imputation = mode_engine_capacity_by_make.get(make, None)
            if imputation is not None:
                warn(f"Updating engine_capacity '{row['engine_capacity']}' to {imputation}: {row['url']}")
            return imputation
        return row['engine_capacity']

    def fill_transmission(row):
        if pd.isna(row['transmission']):
            make = row.get('make', '')
            imputation = mode_transmission_by_make.get(make, None)
            if imputation is not None:
                warn(f"Updating transmission '{row['transmission']}' to {imputation}: {row['url']}")
            return imputation
        return row['transmission']

    df['mileage'] = df.apply(fill_mileage, axis=1)
    df['engine_capacity'] = df.apply(fill_engine_capacity, axis=1)
    df['transmission'] = df.apply(fill_transmission, axis=1)

    return df.to_dict(orient='records')
