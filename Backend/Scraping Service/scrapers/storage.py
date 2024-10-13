class Storage(object):
    """This class is used to store the vehicle Details and stats"""

    def __init__(self):
        self.vehicles = []
        self.stats = {}

    def add(self, vehicle):
        self.vehicles.append(vehicle)

    def add_stat(self, stats):
        self.stats = stats

    def get(self):
        return self.vehicles

    def get_stats(self):
        return self.stats

    def clear(self):
        self.vehicles.clear()
        self.stats.clear()
