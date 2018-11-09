from vehicle import Vehicle


class Bus(Vehicle):

    def __init__(self):
        super().__init__()
        self.passengers = []

    def add_gruop(self, passengers):
        self.passengers.extend(passengers)


bus = Bus()

bus.add_warning('Some warning')

print(bus.get_warnings())

print(bus)