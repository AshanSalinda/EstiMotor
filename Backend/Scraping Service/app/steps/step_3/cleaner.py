import re
from datetime import datetime
from app.data.parameters import *


def clean_vehicle_data(vehicle):
    """Clean a single vehicle's data."""

    return {
        'url': vehicle.get('url', ''),
        PRICE: clean_numbers(vehicle.get(PRICE, '')),
        MILEAGE: clean_numbers(vehicle.get(MILEAGE, '')),
        YOM: clean_yom(vehicle.get(YOM, '')),
        ENGINE_CAPACITY: clean_numbers(vehicle.get(ENGINE_CAPACITY, '')),
        MAKE: clean_make(vehicle.get(MAKE, '')),
        TRANSMISSION: clean_transmission(vehicle.get(TRANSMISSION, '')),
        FUEL_TYPE: clean_fuel_type(vehicle.get(FUEL_TYPE, '')),
        MODEL: clean_model(vehicle.get(MODEL, '')),
    }


def clean_numbers(value):
    """Remove symbols, commas, and convert to integer by truncating decimal."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(float(value))

    value_str = str(value)

    # Keep only dots that are surrounded by digits (e.g., "123.45")
    value_str = re.sub(r'(?<!\d)\.|\.?(?!\d)', '', value_str)

    # Remove all characters except digits and dots
    value_str = re.sub(r'[^0-9.]', '', value_str)

    # If multiple valid dots exist, keep the last one only
    if value_str.count('.') > 1:
        *rest, last = value_str.split('.')
        value_str = ''.join(rest) + '.' + last

    try:
        return int(float(value_str))
    except ValueError:
        return None


def clean_yom(yom):
    """Ensure YOM is a valid 4-digit year."""
    cleaned_year = clean_numbers(yom)

    if cleaned_year is None:
        return None
    try:
        if 1900 <= cleaned_year <= datetime.now().year:
            return cleaned_year
    except (ValueError, TypeError):
        return None

def clean_transmission(transmission):
    """Normalize transmission case and values."""
    if not transmission:
        return None

    transmission_str = str(transmission).strip().lower()

    if 'auto' in transmission_str:
        return 'automatic'
    elif 'manual' in transmission_str:
        return 'manual'
    else:
        print("Not Supported transmission: ", transmission_str)
        return None

def clean_fuel_type(fuel_type):
    """Normalize fuel type case and values."""
    if not fuel_type:
        return None

    fuel_str = str(fuel_type).strip().lower()
    valid_fuels = ['petrol', 'diesel', 'electric', 'hybrid']
    return fuel_str if fuel_str in valid_fuels else None

def clean_model(model):
    """Trim whitespace and normalize model name."""
    return model.strip().title() if model else None

def clean_make(make):
    """Trim whitespace and normalize make name."""
    return make.strip().title() if make else None
