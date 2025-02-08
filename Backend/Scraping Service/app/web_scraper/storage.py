class Storage(object):
    """A static class for store the vehicle Details and stats"""
    
    _vehicles = []
    _stats = {}
    
    def __new__(cls, *args, **kwargs):
        raise TypeError("Storage is a static class and cannot be instantiated. Use class methods instead.")

    @classmethod
    def add_vehicle(cls, vehicle):
        cls._vehicles.append(vehicle)

    @classmethod
    def add_stat(cls, stats):
        cls._stats = stats

    @classmethod
    def get_vehicles(cls):
        return cls._vehicles

    @classmethod
    def get_stats(cls):
        return cls._stats

    @classmethod
    def clear(cls):
        cls._vehicles.clear()
        cls._stats.clear()
