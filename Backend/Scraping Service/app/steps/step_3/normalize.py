import re
import pandas as pd
from datetime import datetime
from app.data.parameters import *
from app.utils.logger import warn
from app.utils.message_queue import MessageQueue


def normalize_vehicle_data(vehicle) -> dict:
    """Clean and standardize a single vehicle's data."""

    url = vehicle.get('url', '')

    return {
        'url': url,
        PRICE: clean_numbers(vehicle.get(PRICE, '')),
        MILEAGE: clean_numbers(vehicle.get(MILEAGE, '')),
        YOM: clean_yom(vehicle.get(YOM, '')),
        ENGINE_CAPACITY: clean_numbers(vehicle.get(ENGINE_CAPACITY, '')),
        MAKE: clean_make(vehicle.get(MAKE, '')),
        TRANSMISSION: clean_transmission(vehicle.get(TRANSMISSION, ''), url),
        FUEL_TYPE: clean_fuel_type(vehicle.get(FUEL_TYPE, ''), url),
        MODEL: clean_model(vehicle.get(MODEL, '')),
    }


def clean_numbers(value) -> int | None:
    """Remove symbols, commas, and convert to integer by truncating decimal."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(float(value))

    # Remove all non-digit characters, except periods surrounded by digits
    value_str = str(value).strip()
    value_str = re.sub(r'(?<!\d)\.(?!\d)', '', value_str)
    value_str = re.sub(r'[^\d.]', '', value_str)

    try:
        return int(float(value_str))
    except ValueError:
        return None


def clean_yom(yom) -> int | None:
    """Ensure YOM is a valid 4-digit year."""
    cleaned_year = clean_numbers(yom)

    if cleaned_year is None:
        return None
    try:
        if 1900 <= cleaned_year <= datetime.now().year:
            return cleaned_year
    except (ValueError, TypeError):
        return None


def clean_transmission(transmission, url) -> str | None:
    """Normalize transmission case and values."""
    if not transmission:
        return None

    transmission_str = str(transmission).strip().lower()

    if 'auto' in transmission_str:
        return 'automatic'
    elif 'manual' in transmission_str:
        return 'manual'
    else:
        print(f"Not Supported transmission: {transmission_str} for {url}")
        return None


def clean_fuel_type(fuel_type, url) -> str | None:
    """Normalize fuel type case and values."""
    if not fuel_type:
        return None

    fuel_str = str(fuel_type).strip().lower()
    valid_fuels = ['petrol', 'diesel', 'electric', 'hybrid']

    if fuel_str in valid_fuels:
        return fuel_str
    else:
        print(f"Not Supported fuel type: {fuel_type} for {url}")
        return None


def clean_model(model) -> str | None:
    """Normalize model case and values."""
    return model.strip().title() if model else None


def clean_make(make) -> str | None:
    """Normalize make case and values."""
    return make.strip().title() if make else None


def null_cleanup(vehicles: list, progress_manager) -> list[dict]:
    """
    Handle null values in vehicle dataset:
      1. Drop records missing essential fields (PRICE, YOM, MAKE).
      3. Fill remaining optional fields with placeholders
         to avoid leaving nulls in the dataset.
    """

    essential_fields = [PRICE, YOM, MAKE]

    # Convert vehicles list into DataFrame for easier processing
    df = pd.DataFrame(vehicles)

    # Keep only rows where essential fields are not null
    df_cleaned = df.dropna(subset=essential_fields).copy()

    # Identify and log dropped rows
    dropped_rows = df.loc[~df.index.isin(df_cleaned.index)]
    if not dropped_rows.empty:
        count = 0
        for _, row in dropped_rows.iterrows():
            count += 1
            missing = [field for field in essential_fields if pd.isna(row[field])]
            url = row.get("url", "N/A")
            progress_manager.log({'action': 'Dropped', 'message': f'Missing {missing[0]}', 'url': url})
        progress_manager.add_dropped(count)

    # Count nulls before filling
    null_counts = df_cleaned.isnull().sum()

    # Fill optional fields with placeholders instead of null
    df_cleaned[MILEAGE] = df_cleaned[MILEAGE].fillna(-1)
    df_cleaned[ENGINE_CAPACITY] = df_cleaned[ENGINE_CAPACITY].fillna(-1)
    df_cleaned[FUEL_TYPE] = df_cleaned[FUEL_TYPE].fillna('N/A')
    df_cleaned[MODEL] = df_cleaned[MODEL].fillna('N/A')
    df_cleaned[TRANSMISSION] = df_cleaned[TRANSMISSION].fillna('N/A')

    # Log how many placeholders were filled
    for field in [MILEAGE, ENGINE_CAPACITY, FUEL_TYPE, MODEL, TRANSMISSION]:
        if null_counts.get(field, 0) > 0:
            placeholder = '-1' if field in [MILEAGE, ENGINE_CAPACITY] else 'N/A'
            warn(f"Filled {null_counts[field]} nulls in {field} with {placeholder}")
            progress_manager.add_modified(int(null_counts[field]))

    # Convert cleaned DataFrame back to list of dicts
    return df_cleaned.to_dict(orient="records")
