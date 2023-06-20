import copy
from abc import abstractmethod
from random import randint


def map_pos_to_arr_ind(position: tuple):
    if position[1] < 21:
        return position[0], 0
    if position[1] < 28:
        return position[0], 1
    if position[1] < 34:
        return position[0], 2
    return position[0], 3


class RoadVehicle:
    # all in cell units
    acceleration = 0
    width = 0
    length = 0
    max_speed = 28  # 50km/h = 14m/s

    look_ahead_variable = 30

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
        x, y = map_pos_to_arr_ind(self.position)
        i = 0

        while RoadVehicle.look_ahead_variable > i > 0 and i < len(self.map[0]):
            if isinstance(self.map[x + i][y], Crossing):  # tutaj zamienic na PedstrainCrossing
                if self.map[x + i][y].open is False:
                    break
            if self.map[x + i][y] is None:
                break

            if y == 0:
                i -= 1
            else:
                i += 1

        return abs(i)

    def look_ahead_moving_obstacle(self) -> int:
        x, y = map_pos_to_arr_ind(self.position)
        i = 0

        while RoadVehicle.look_ahead_variable > i > 0 and i < len(self.map[0]):
            if isinstance(self.map[x + i][y], RoadVehicle):
                i = (abs(i) - self.map[x + i][y].length) + (abs(i) - self.map[x + i][y].length) * self.map[x + i][
                    y].speed
                # distance + disctance*speed of next vehicle
                break
            if y == 0:
                i -= 1
            else:
                i += 1
        return abs(i)

    def vehicle_acceleration(self, distance_to_obstacle):

        if self.speed < self.max_speed and self.speed + self.acceleration < distance_to_obstacle:
            self.speed = min(self.speed + self.acceleration, self.max_speed)

    def vehicle_deacceleration(self, distance_to_obstacle):
        if self.speed > distance_to_obstacle:
            self.speed = max(self.speed - self.acceleration, 0)

    def move_vehicle(self):
        distance_to_obstacle = min(self.look_ahead_moving_obstacle(), self.look_ahead_static_obstacle())
        self.vehicle_acceleration(distance_to_obstacle)
        self.vehicle_deacceleration(distance_to_obstacle)

        if isinstance(self, Car):
            if self.will_turn is False:
                self.change_lane()


class Crossing:
    """
    obiekt - przejscie dla pieszych, ustawia sie w nim czy przejscie jest otwrte czy zamkanięte
    (open == true -> auto moze jechac)

    Prawdopodobnie zamienic na obiekty klasy PedastrainCrossing
    """

    def __init__(self, position: (int, int), open: bool):
        self.position = position
        self.open = open


class Car(RoadVehicle):
    def __init__(self, position, map, will_turn=False):
        super().__init__(position, map)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True
        self.will_turn = will_turn
        self.max_speed = 28

    def look_other_lane_ahead_and_behind(self, x: int, y: int) -> (int, int):

        ahead = 0

        while RoadVehicle.look_ahead_variable > ahead:
            if isinstance(self.map[x + ahead][y], RoadVehicle):
                ahead = (abs(ahead) - self.map[x + ahead][y].length) * self.map[x + ahead][y].speed
                break
            if self.map[x + ahead][y] is None:
                break
            ahead += 1

        behind = 0

        while behind < RoadVehicle.look_ahead_variable:

            if isinstance(self.map[x - behind][y], RoadVehicle):
                behind = (abs(behind) - self.length) * self.map[x - behind][y].speed
                break
            if self.map[x - behind][y] is None:
                behind = RoadVehicle.look_ahead_variable
                break

            behind += 1

        return behind, ahead


def crossing_incoming(self, x: int, y: int) -> int:
    ahead = 0
    while RoadVehicle.look_ahead_variable > ahead:
        if self.map[x + ahead][y] is None:
            break
        ahead += 1
    return ahead


def change_lane(self):
    x, y = map_pos_to_arr_ind(self.position)

    if y == 1:
        # middle pas, sprawdzic czy nie trzeba juz zjedzac, czy nie zbliza sie wysepka
        crossing_distance = self.crossing_incoming(x, y)  # zblizanie sie wysepki

        if crossing_distance <= RoadVehicle.look_ahead_variable:
            behind, ahead = self.look_other_lane_ahead_and_behind(x, y + 1)

            if behind <= self.speed and self.speed <= ahead:
                self.position = (x, y + 1)
                # changing lane
                # todo zmienic jego pozycjie w tablicy

        pass

    if y == 2 and self.map[y - 1][x] is None:
        # lewy pas, sprawdzenie czy mozna zjechac na srodek
        behind, ahead = self.look_other_lane_ahead_and_behind(x, y - 1)

        if behind >= self.speed and self.speed <= ahead:
            self.position = (x, y - 1)
            # changing lane
            # todo zmienic jego pozycjie w tablicy


class Bus(RoadVehicle):
    def __init__(self, position, map):
        super().__init__(position, map)
        self.acceleration = 3
        self.width = 5
        self.length = 24
        self.stops = True
        self.preferred_lane = 'r'
        self.max_speed = 24


class BigBus(RoadVehicle):  # coach in documentation
    def __init__(self, position, map):
        super().__init__(position, map)
        self.acceleration = 3
        self.width = 5
        self.length = 36
        self.stops = True
        self.preferred_lane = 'r'
        self.max_speed = 24


class Truck(RoadVehicle):
    def __init__(self, position, map):
        super().__init__(position, map)
        self.acceleration = 2
        self.width = 6
        self.length = 22
        self.max_speed = 22


class Scooter(RoadVehicle):
    def __init__(self, position, map):
        super().__init__(position, map)
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
    def __init__(self, width_range, up_spawn_range, down_spawn_range, type, spawn_prob):
        self.spawn_prob = spawn_prob
        self.type = type
        self.width_range = width_range
        self.up_spawn_range = up_spawn_range
        self.down_spawn_range = down_spawn_range
        self.total_width = width_range[1] - width_range[0] + 1
        self.total_height = down_spawn_range[1] - up_spawn_range[0] + 1
        self.map = []
        for i in range(self.total_width):
            self.map.append([])
            for j in range(self.total_height):
                self.map[i].append([])

    def spawn_pedestrian_up(self):
        # todo count amount of pedestrians to avoid situation with overfilling
        x = randint(0, self.total_width - 1)
        y = randint(self.up_spawn_range[0], self.up_spawn_range[1]) - self.up_spawn_range[0]
        while len(self.map[x][y]) != 0:
            x = randint(0, self.total_width - 1)
            y = randint(self.up_spawn_range[0], self.up_spawn_range[1]) - self.up_spawn_range[0]
        self.map[x][y].append(Pedestrian((x, y), -1))

    def spawn_pedestrian_down(self):
        # todo count amount of pedestrians to avoid situation with overfilling
        x = randint(0, self.total_width - 1)
        y = randint(self.down_spawn_range[0], self.down_spawn_range[1]) - self.up_spawn_range[0]
        while len(self.map[x][y]) != 0:
            x = randint(0, self.total_width - 1)
            y = randint(self.down_spawn_range[0], self.down_spawn_range[1]) - self.up_spawn_range[0]
        self.map[x][y].append(Pedestrian((x, y), 1))

    def move(self):
        map_copy = copy.deepcopy(self.map)
        self.map = [[[] for _ in range(self.total_height)] for _ in range(self.total_width)]
        for i in range(self.total_width):
            for j in range(self.total_height):
                if len(map_copy[i][j]) != 0:
                    for elem in map_copy[i][j]:
                        # self.map[i][j] = None
                        if (elem.direction == -1 and j >= self.down_spawn_range[0] - self.up_spawn_range[0] - 1) \
                                or (elem.direction == 1 and j <= self.up_spawn_range[1] - self.up_spawn_range[0]):
                            continue
                        self.map[i][j - (elem.direction * elem.speed)].append(elem)
                        # self.map[i][j - map_copy[i][j]].position = (i, j - map_copy[i][j])

    def update_speed(self):
        for i in range(self.total_width):
            for j in range(self.total_height):
                if len(self.map[i][j]) != 0:
                    for elem in self.map[i][j]:
                        elem.speed = min(Pedestrian.max_speed, elem.speed + 1)
                    # if randint(0, 10) <= 3:
                    #     self.map[i][j].speed = max(Pedestrian.max_speed, self.map[i][j].speed + 1)

    def iterate(self):
        self.update_speed()
        self.move()
