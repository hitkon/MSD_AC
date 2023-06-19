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
            if self.map[y][x + 1] is None:
                break

            if y == 0:
                i -= 1
            else:
                i += 1

        return abs(i)

    def look_ahead_moving_obstacle(self) -> int:
        x, y = self.position
        i = 0

        while RoadVehicle.look_ahead_variable > i > 0 and i < len(self.map[0]):
            if isinstance(self.map[y][x + i], RoadVehicle):
                i = (abs(i) - self.map[y][x + i].length) + (abs(i) - self.map[y][x + i].length) * self.map[y][
                    x + i].speed
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
    """

    def __init__(self, position: (int, int), open: bool):
        self.position = position
        self.open = open


class Car(RoadVehicle):
    def __init__(self, position, will_turn=False):
        super().__init__(position)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True
        self.will_turn = will_turn
        self.max_speed = 28

    def look_other_lane_ahead_and_behind(self, x: int, y: int) -> (int, int):

        ahead = 0

        while RoadVehicle.look_ahead_variable > ahead:
            if isinstance(self.map[y][x + ahead], RoadVehicle):
                ahead = (abs(ahead) - self.map[y][x + ahead].length) + (abs(ahead) - self.map[y][x + ahead].length) * \
                        self.map[y][
                            x + ahead].speed
                break
            if self.map[y][x + ahead] is None:
                break
            ahead += 1

        behind = 0

        while behind < RoadVehicle.look_ahead_variable:

            if isinstance(self.map[y][x - behind], RoadVehicle):
                behind = (abs(behind) - self.map[y][x - behind].length) + (
                        abs(behind) - self.map[y][x - behind].length) * self.map[y][x - behind].speed
                break
            if self.map[y][x - behind] is None:
                behind = RoadVehicle.look_ahead_variable
                break

            behind += 1

        return behind, ahead

    def crossing_incoming(self, x: int, y: int) -> int:
        ahead = 0
        while RoadVehicle.look_ahead_variable > ahead:
            if self.map[y][x + ahead] is None:
                break
            ahead += 1
        return ahead

    def change_lane(self):

        x, y = self.position

        if y == 1:
            # middle pas, sprawdzic czy nie trzeba juz zjedzac, czy nie zbliza sie wysepka
            crossing_distance = self.crossing_incoming(x, y)  # zblizanie sie wysepki

            if crossing_distance <= RoadVehicle.look_ahead_variable:
                behind, ahead = self.look_other_lane_ahead_and_behind(x, y + 1)

                if behind >= self.speed and self.speed <= ahead:
                    self.position = (x, y + 1)

            pass

        if y == 2 and self.map[y - 1][x] is None:
            #lewy pas, sprawdzenie czy mozna zjechac na srodek
            behind, ahead = self.look_other_lane_ahead_and_behind(x, y - 1)

            if behind >= self.speed and self.speed <= ahead:
                self.position = (x, y - 1)


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
    def __init__(self, width_range, up_spawn_range, down_spawn_range, type, spawn_prob):
        self.spawn_prob = spawn_prob
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




