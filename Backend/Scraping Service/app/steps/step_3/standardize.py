import re
import pandas as pd
from datetime import datetime
from app.data.parameters import *


def standardize_vehicle_data(vehicle) -> dict:
    """"Clean and standardize a single vehicle's data."""

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
    value_str = str(value)
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


def final_cleanup(vehicles: list) -> list[dict]:
    essential_fields = [PRICE, YOM, MAKE]

    df = pd.DataFrame(vehicles)
    df_cleaned = df.dropna(subset=essential_fields)

    df[MILEAGE] = df[MILEAGE].fillna('unknown')
    df[ENGINE_CAPACITY] = df[ENGINE_CAPACITY].fillna('unknown')
    df[FUEL_TYPE] = df[FUEL_TYPE].fillna('unknown')
    df[MODEL] = df[MODEL].fillna('unspecified')
    df[TRANSMISSION] = df[TRANSMISSION].fillna('unknown')

    return df_cleaned.to_dict(orient='records')