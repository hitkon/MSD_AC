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
    def __init__(self, position):
        self.position = position
        self.speed = 0
        self.preferred_lane = 'l'

    def look_ahead_static_obstacle(self, map: list) -> int:
        x, y = self.position
        i = 1

        while i < RoadVehicle.look_ahead_variable:
            # todo zalozenie, jak pieszy bedzie wchodzic na pasy bez swietal tez tam ustawic crossign_closed?
            if map[x + i][y] == 6:
                break
            if map[x + i][y] == 5:
                break

            i += 1

        return i

    def look_ahead_moving_obstacle(self, map: list) -> int:
        #todo check speeed of obstacle before us and multiply i
        x, y = self.position
        i = 1

        while i < RoadVehicle.look_ahead_variable:
            if map[x + i][y] == 4:
                break
            i += 1
        return i

    def vehicle_acceleration(self):
        pass
        if self.speed < self.max_speed:
            self.speed = min(self.speed + self.acceleration, self.max_speed)

    def vehicle_deacceleration(self, map: list):
        distance_to_obstacle = min(self.look_ahead_moving_obstacle(map), self.look_ahead_static_obstacle(map))
        if self.speed > distance_to_obstacle:
            self.speed =  max(self.speed - self.acceleration, 0)



class Car(RoadVehicle):
    def __init__(self, position):
        super.__init__(position)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True
        self.max_speed = 28


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
