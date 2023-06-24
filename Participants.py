import random
from abc import abstractmethod


def is_vehicle(obj) -> bool:
    if obj is None or obj == 0:
        return False
    return True


def map_pos_to_arr_ind(position: tuple):
    if position[1] < 21:
        return position[0], 0
    if position[1] < 28:
        return position[0], 1
    if position[1] < 34:
        return position[0], 2
    return position[0], 3


bus_stop_cord = 330
max_veh_len = 36
max_veh_speed = 28


class RoadVehicle:
    # all in cell units
    acceleration = 0
    width = 0
    length = 0
    max_speed = 28  # 50km/h = 14m/s

    look_ahead_variable = 30

    can_turn = False  # True if the vehicle can turn on the crossings
    stops = False  # True if the vehicle stops at the bus stop

    @abstractmethod
    def __init__(self, position: (int, int), map: list):
        self.position = position
        self.speed = 0
        self.map = map
        self.preferred_lane = 'l'  # 'l' for left, 'r' for right
        self.will_switch = False
        self.iters_to_wait = 25    # how much time does a bus need to wait on a bus stop
        self.will_turn = False
        self.chosen_route = 0      # for choosing Budryka/Kawiory (0/1) turn

    def distance_to_static_obstacle(self) -> int:
        # todo check pedestrians
        x, y = map_pos_to_arr_ind(self.position)

        if y == 0:
            pass
        else:
            pass
        if self.will_turn:
            if self.chosen_route == 0:
                return abs(660 - x) + 1
            else:
                return abs(742 - x) + 1
        if self.stops and y == 2:
            if x < bus_stop_cord:
                return bus_stop_cord - x + 1
            if x == bus_stop_cord and self.iters_to_wait > 0:
                self.iters_to_wait -= 1
                return 0

        return 2*(self.speed + self.acceleration + 1 + max_veh_len)
    #     i = 0
    #
    #     while RoadVehicle.look_ahead_variable > i > 0 and i < len(self.map[0]):
    #         if isinstance(self.map[x + i][y], Crossing):  # tutaj zamienic na PedstrainCrossing
    #             if self.map[x + i][y].open is False:
    #                 break
    #         if self.map[x + i][y] is None:
    #             break
    #
    #         if y == 0:
    #             i -= 1
    #         else:
    #             i += 1
    #
    #     return abs(i)

    def distance_to_moving_obstacle(self) -> int:
        x, y = map_pos_to_arr_ind(self.position)
        if y == 0:
            for i in range(1, self.speed + self.acceleration + 1 + max_veh_len):
                if x - i < 0:
                    return self.speed + self.acceleration + 1 + max_veh_len
                if is_vehicle(self.map[x-i][y]):
                    return i - self.map[x-i][y].length
        else:
            found_so_far = self.speed + self.acceleration + 1 + max_veh_len
            for i in range(1, self.speed + self.acceleration + 1 + max_veh_len):
                if x+i >= len(self.map):
                    break
                if is_vehicle(self.map[x+i][y]):
                    found_so_far = i - self.map[x+i][y].length
                    break
            if self.will_switch:
                if y == 1:
                    y += 1
                else:
                    y -= 1
                for i in range(0, -Car.max_speed, -1):
                    if x+i >= 0 and self.map[x+i][y] is None:
                        break
                    if x+i >= 0 and is_vehicle(self.map[x+i][y]):
                        return 0
                for i in range(1, self.speed + self.acceleration + 1 + max_veh_len):
                    if x+i >= len(self.map):
                        return min(self.speed + self.acceleration + 1 + max_veh_len, found_so_far)
                    if x+i >= 0 and is_vehicle(self.map[x+i][y]):
                        return min(i - self.map[x+i][y].length, found_so_far)
                return found_so_far
            else:
                return found_so_far
        return self.speed + self.acceleration + 1 + max_veh_len

    def update_will_switch(self):
        self.will_switch = False
        if self.preferred_lane == 'r':
            return
        x, y = map_pos_to_arr_ind(self.position)
        if y == 0:
            return
        if y == 1:
            for i in range(1, self.speed + self.acceleration + 1):
                if x + i >= len(self.map):
                    return
                if self.map[x+i][y] is None:
                    self.will_switch = True
                    return
            return
        if y == 2:
            for i in range(1, self.speed + self.acceleration + 1):
                if x + i > len(self.map):
                    return
                if self.map[x+i][y-1] is not None:
                    self.will_switch = True
                    return

    def accelerate(self, distance_to_obstacle):
        if self.speed < self.max_speed and self.speed < distance_to_obstacle:
            self.speed = min(self.speed + self.acceleration, self.max_speed, distance_to_obstacle - 1)

    def brake(self, distance_to_obstacle):
        if self.speed >= distance_to_obstacle:
            self.speed = max(min(self.speed - self.acceleration, distance_to_obstacle-1), 0)

    # def move_vehicle(self):
    #     distance_to_obstacle = min(self.look_ahead_moving_obstacle(), self.look_ahead_static_obstacle())
    #     self.accelerate(distance_to_obstacle)
    #     self.brake(distance_to_obstacle)
    #
    #     if isinstance(self, Car):
    #         if self.will_turn is False:
    #             self.change_lane()

    def set_speed(self):
        # todo check if pedestrian is on the way
        self.update_will_switch()
        dist = min(self.distance_to_moving_obstacle(), self.distance_to_static_obstacle()//2 + 1)
        self.accelerate(dist)
        self.brake(dist)
        if self.speed == 0 and 100 < self.position[0] < 1300:
            a = 3
        # print("distance to obstacle:", dist, "\nSpeed:", self.speed)


class Car(RoadVehicle):
    def __init__(self, position, map, will_turn=False):
        super().__init__(position, map)
        self.acceleration = 4
        self.width = 4
        self.length = 9
        self.can_turn = True
        # self.will_turn = will_turn
        self.max_speed = 28
        self.chosen_route = random.randint(0, 1) == 1

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
        if random.randint(0, 1) == 0:
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
        self.chosen_route = random.randint(0, 1) == 1


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



