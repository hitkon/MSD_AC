import copy
from abc import abstractmethod
from random import randint


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
        super().__init__(position)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True
        self.max_speed = 28


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
    max_speed = 2

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


class Bicycle:
    width = 2
    length = 4
    speed = 0
    max_speed = 6

    def __init__(self, position):
        self.position = position



class PedestrianCrossing:
    def __init__(self, width_range, up_spawn_range, down_spawn_range, type):
        self.type = type
        self.width_range = width_range
        self.up_spawn_range = up_spawn_range
        self.down_spawn_range = down_spawn_range
        self.total_width = width_range[1] - width_range[0] + 1
        self.total_height = down_spawn_range[1] - up_spawn_range[0] +1
        self.map = []
        for i in range(self.total_width):
            self.map.append([])
            for j in range(self.total_height):
                self.map[i].append(None)
    def spawn_pedestrian_up(self):
        #todo count amount of pedestrians to avoid situation with overfilling
        x = randint(0, self.total_width - 1)
        y = randint(self.up_spawn_range[0], self.up_spawn_range[1]) - self.up_spawn_range[0]
        while self.map[x][y] is not None:
            x = randint(0, self.total_width-1)
            y = randint(self.up_spawn_range[0], self.up_spawn_range[1]) - self.up_spawn_range[0]
        self.map[x][y] = Pedestrian((x,y), -1)


    def spawn_pedestrian_down(self):
        # todo count amount of pedestrians to avoid situation with overfilling
        x = randint(0, self.total_width-1)
        y = randint(self.down_spawn_range[0], self.down_spawn_range[1]) - self.up_spawn_range[0]
        while self.map[x][y] is not None:
            x = randint(0, self.total_width-1)
            y = randint(self.down_spawn_range[0], self.down_spawn_range[1]) - self.up_spawn_range[0]
        self.map[x][y] = Pedestrian((x, y), 1)

    def move(self):
        map_copy = copy.deepcopy(self.map)
        self.map = [[None for _ in range(self.total_height)] for _ in range(self.total_width)]
        for i in range(self.total_width):
            for j in range(self.total_height):
                if map_copy[i][j] is not None:
                    # self.map[i][j] = None
                    if (map_copy[i][j].direction == -1 and j >= self.down_spawn_range[0] - self.up_spawn_range[0] - 1) \
                            or (map_copy[i][j].direction == 1 and j <= self.up_spawn_range[1] - self.up_spawn_range[0]):
                        continue
                    self.map[i][j - (map_copy[i][j].direction * map_copy[i][j].speed)] = (map_copy[i][j])
                    # self.map[i][j - map_copy[i][j]].position = (i, j - map_copy[i][j])

    def update_speed(self):
        for i in range(self.total_width):
            for j in range(self.total_height):
                if self.map[i][j] is not None:
                    self.map[i][j].speed = min(Pedestrian.max_speed, self.map[i][j].speed+1)
                    # if randint(0, 10) <= 3:
                    #     self.map[i][j].speed = max(Pedestrian.max_speed, self.map[i][j].speed + 1)
    def iterate(self):
        self.update_speed()
        self.move()




