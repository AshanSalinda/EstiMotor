import pandas as pd
from datetime import datetime


def impute_missing_fields(cleaned_vehicles: list, imputation_stats: dict, progress_manager):
    median_mileage_by_year = imputation_stats.get("median_mileage_by_year", {})
    mode_engine_capacity_by_make = imputation_stats.get("mode_engine_capacity_by_make", {})
    mode_transmission_by_make = imputation_stats.get("mode_transmission_by_make", {})
    current_year = datetime.now().year

    df = pd.DataFrame(cleaned_vehicles)

    def fill_mileage(row):
        if pd.isna(row['mileage']):
            year = row.get('year')
            imputation = 0 if year == current_year else median_mileage_by_year.get(str(year), None)
            if imputation is not None:
                progress_manager.add_modified()
                progress_manager.log({'action': 'Modified', 'message': f'mileage to {imputation}', 'url': row['url']})
            return imputation
        return row['mileage']

    def fill_engine_capacity(row):
        if pd.isna(row['engine_capacity']):
            make = row.get('make', '')
            imputation = mode_engine_capacity_by_make.get(make, None)
            if imputation is not None:
                progress_manager.add_modified()
                progress_manager.log({'action': 'Modified', 'message': f'engine_capacity to {imputation}', 'url': row['url']})
            return imputation
        return row['engine_capacity']

    def fill_transmission(row):
        if pd.isna(row['transmission']):
            make = row.get('make', '')
            imputation = mode_transmission_by_make.get(make, None)
            if imputation is not None:
                progress_manager.add_modified()
                progress_manager.log({'action': 'Modified', 'message': f'transmission to {imputation}', 'url': row['url']})
            return imputation
        return row['transmission']

    df['mileage'] = df.apply(fill_mileage, axis=1)
    df['engine_capacity'] = df.apply(fill_engine_capacity, axis=1)
    df['transmission'] = df.apply(fill_transmission, axis=1)

    return df.to_dict(orient='records')
