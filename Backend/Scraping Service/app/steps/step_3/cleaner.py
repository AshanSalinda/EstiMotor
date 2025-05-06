import re

from app.data.parameters import *


def clean_vehicle_data(vehicle):
    """Clean a single vehicle's data."""

    return {
        'url': vehicle.get('url', ''),
        PRICE: clean_price(vehicle.get(PRICE, '')),
        MILEAGE: clean_mileage(vehicle.get(MILEAGE, '')),
        YOM: clean_yom(vehicle.get(YOM, '')),
        ENGINE_CAPACITY: clean_engine_capacity(vehicle.get(ENGINE_CAPACITY, '')),
        MAKE: clean_make(vehicle.get(MAKE, '')),
        TRANSMISSION: clean_transmission(vehicle.get(TRANSMISSION, '')),
        FUEL_TYPE: clean_fuel_type(vehicle.get(FUEL_TYPE, '')),
        MODEL: clean_model(vehicle.get(MODEL, '')),
    }


def clean_price(price):
    """Remove currency symbols and commas from price and convert to integer."""
    price = re.sub(r'[^\d]', '', price)  # Remove non-digit characters
    return int(price) if price else None


def clean_mileage(mileage):
    """Handle mileage units and convert to integer."""
    mileage = re.sub(r'[^\d]', '', mileage)  # Remove non-digit characters
    return int(mileage) if mileage else None


def clean_yom(yom):
    """Ensure YOM is a valid 4-digit year."""
    try:
        yom = int(yom)
        if 1900 <= yom <= 2100:
            return yom
        else:
            return None
    except ValueError:
        return None


def clean_transmission(transmission):
    """Normalize transmission case and values."""
    transmission = transmission.strip().lower()
    return 'automatic' if 'auto' in transmission.lower() else 'manual' if 'manual' in transmission else None


def clean_fuel_type(fuel_type):
    """Normalize fuel type case and values."""
    fuel_type = fuel_type.strip().lower()
    return fuel_type if fuel_type in ['petrol', 'diesel', 'electric', 'hybrid'] else None


def clean_engine_capacity(engine_capacity):
    """Remove units from engine capacity and convert to integer."""
    engine_capacity = re.sub(r'[^\d]', '', engine_capacity)  # Remove non-digit characters
    return int(engine_capacity) if engine_capacity else None


def clean_model(model):
    """Trim whitespace and normalize model name."""
    return model.strip().title() if model else None


def clean_make(make):
    """Trim whitespace and normalize make name."""
    return make.strip().title() if make else None
