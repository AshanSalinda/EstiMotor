from collections import defaultdict, Counter
import numpy as np

def compute_imputation_stats(vehicles):
    mileage_by_yom = defaultdict(list)
    engine_capacity_by_make = defaultdict(list)
    transmission_by_make = defaultdict(list)

    for vehicle in vehicles:
        yom = clean_yom(vehicle.get(YOM))
        mileage = clean_numbers(vehicle.get(MILEAGE))
        make = clean_make(vehicle.get(MAKE))
        engine_capacity = clean_numbers(vehicle.get(ENGINE_CAPACITY))
        transmission = clean_transmission(vehicle.get(TRANSMISSION))

        if yom and mileage is not None:
            mileage_by_yom[yom].append(mileage)

        if make:
            if engine_capacity is not None:
                engine_capacity_by_make[make].append(engine_capacity)
            if transmission:
                transmission_by_make[make].append(transmission)

    median_mileage = {k: int(np.median(v)) for k, v in mileage_by_yom.items()}
    mode_engine_capacity = {k: Counter(v).most_common(1)[0][0] for k, v in engine_capacity_by_make.items()}
    mode_transmission = {k: Counter(v).most_common(1)[0][0] for k, v in transmission_by_make.items()}

    return median_mileage, mode_engine_capacity, mode_transmission
