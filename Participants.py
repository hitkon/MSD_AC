from abc import abstractmethod




class RoadVehicle:
    # all in cell units
    acceleration = 0
    width = 0
    length = 0
    max_speed = 28  # 50km/h = 14m/s

    look_ahead_variable = 28

    preferred_lane = 'l'  # 'l' for left, 'r' for right
    can_turn = False  # True if the vehicle can turn on the crossings
    stops = False  # True if the vehicle stops at the bus stop

    @abstractmethod
    def __init__(self, position: (int, int), map: list):  # pozacja w tabeli tej malej (3x1400), map (ta na 3x1400)
        self.position = position
        self.speed = 0
        self.map = map
        self.preferred_lane = 'l'

    def look_ahead_static_obstacle(self) -> int:
        x, y = self.position
        i = 0

        while RoadVehicle.look_ahead_variable > i > 0 and i < len(self.map[0]):
            if isinstance(self.map[y][x + i], Crossing):
                if self.map[y][x + i].open is False:
                    break
            if y == 0:
                i -= 1
            else:
                i += 1

        return i

    def look_ahead_moving_obstacle(self) -> int:
        x, y = self.position
        i = 0

        while RoadVehicle.look_ahead_variable > i > 0 and i < len(self.map[0]):
            if isinstance(self.map[y][x + i], RoadVehicle):
                i += i * self.map[y][x + 1].speed
                break
            if y == 0:
                i -= 1
            else:
                i += 1
        return i

    def vehicle_acceleration(self):
        distance_to_obstacle = min(self.look_ahead_moving_obstacle(), self.look_ahead_static_obstacle())
        if self.speed < self.max_speed and self.speed + self.acceleration < distance_to_obstacle:
            self.speed = min(self.speed + self.acceleration, self.max_speed)

    def vehicle_deacceleration(self):
        distance_to_obstacle = min(self.look_ahead_moving_obstacle(), self.look_ahead_static_obstacle())
        if self.speed > distance_to_obstacle:
            self.speed = max(self.speed - self.acceleration, 0)

    def move_vehicle(self):
        pass
        self.vehicle_acceleration()
        self.vehicle_deacceleration()

        if isinstance(self, Car):
            self.change_lane()



class Crossing:
    """
    obiekt - przejscie dla pieszych, ustawia sie w nim czy przejscie jest otwrte czy zamkanięte
    (open == true -> auto moze jechac)
    """

    def __init__(self, position: (int, int), open: bool):
        self.position = position
        self.open = open


class Car(RoadVehicle):
    def __init__(self, position):
        super().__init__(position)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True
        self.max_speed = 28


    def change_lane(self):
        #make implementation
        pass


class Bus(RoadVehicle):
    def __init__(self, position):
        super().__init__(position)
        self.acceleration = 3
        self.width = 5
        self.length = 24
        self.stops = True
        self.preferred_lane = 'r'
        self.max_speed = 24


class BigBus(RoadVehicle):
    def __init__(self, position):
        super().__init__(position)
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
        super().__init__(position)
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
