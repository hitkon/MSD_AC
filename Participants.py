from abc import abstractmethod


class RoadVehicle:
    # all in cell units
    speed = 0
    acceleration = 0
    width = 0
    length = 0
    max_speed = 28            # 50km/h = 14m/s

    preferred_lane = 'l'      # 'l' for left, 'r' for right
    can_turn = False          # True if the vehicle can turn on the crossings
    stops = False             # True if the vehicle stops at the bus stop

    @abstractmethod
    def __init__(self, position):
        self.position = position


class Car(RoadVehicle):
    def __init__(self, position):
        super.__init__(position)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True


class Bus(RoadVehicle):
    def __init__(self, position):
        super.__init__(position)
        self.acceleration = 3
        self.width = 5
        self.length = 24
        self.stops = True
        self.preferred_lane = 'r'
        self.max_speed = 24


class BigBus(RoadVehicle):
    def __init__(self, position):
        super.__init__(position)
        self.acceleration = 3
        self.width = 5
        self.length = 36
        self.stops = True
        self.preferred_lane = 'r'
        self.max_speed = 24


class Truck(RoadVehicle):
    def __init__(self, position):
        super().__init__(position)
        self.acceleration = 2
        self.width = 6
        self.length = 22
        self.max_speed = 22


class Scooter(RoadVehicle):
    def __init__(self, position):
        super.__init__(position)
        self.acceleration = 3
        self.width = 2
        self.length = 4
        self.can_turn = True


class Pedestrian:
    width = 1
    length = 1
    speed = 0
    max_speed = 3

    def __init__(self, position):
        self.position = position


class Bicycle:
    width = 2
    length = 4
    speed = 0
    max_speed = 6

    def __init__(self, position):
        self.position = position

