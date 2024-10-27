
class Storage(object):
    """This is a singleton class, used to store the vehicle Details and stats"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Storage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.vehicles = []
            self.stats = {}
            self.initialized = True

    def add(self, vehicle):
        self.vehicles.append(vehicle)

    def add_stat(self, spider, stats):
        print(f"Adding stats for {spider}: {stats}")
        self.stats[spider] = stats

    def get(self):
        return self.vehicles

    def get_stats(self):
        return self.stats

    def clear(self):
        self.vehicles.clear()
        self.stats.clear()
