import copy
import queue
from collections import namedtuple
from Participants import *
from Crossings import *

Fraction = namedtuple('Fraction', ['numerator', 'denominator'])


def rand_with_probability(prob: Fraction):
    return randint(1, prob[1]) <= prob[0]


class Engine:
    # todo real values
    # probability of turn
    prob_budryka = Fraction(1, 10)
    prob_kawiory = Fraction(1, 10)
    prob_kijowska = Fraction(1, 3)

    crossing_open_duration = 40
    crossing_close_duration = 19

    def __init__(self, map: list, pedestrian_arreas: list):
        self.map_w = len(map)
        self.map_h = len(map[0])
        self.map = map
        self.crossing_closed = False
        self.iter_counter = 0
        self.budryka_cars = [[], []]
        self.kawiory_cars = [[], []]
        self.kijowska_to_spawn = queue.Queue()
        self.ak_to_spawn = queue.Queue()
        self.pedestrian_areas = pedestrian_arreas
        self.cars = [[0 for _ in range(3)] for i in range(self.map_w)]
        two_lanes = [(0, 263), (613, 657), (1168, 1215)]
        crossings = [(230,255),(622,645),(1181,1202)] #wspolrzedne przejsc z map0
        for tup in two_lanes:
            for i in range(tup[0], tup[1]):
                self.cars[i][1] = None

    def is_occupied(self, x: int, y: int) -> bool:   # should work
        x_ind, y_ind = map_pos_to_arr_ind((x, y))
        if self.cars[x_ind][y_ind] != 0:
            return True
        if y_ind == 0:
            for i in range(1, min(1 + BigBus.length, x_ind + 1)):
                if is_vehicle(self.cars[x_ind-i][y_ind]):
                    car = self.cars[x_ind-i][y_ind]
                    dist = i
                    return dist > car.length
            return False
        else:
            for i in range(1, min(1 + BigBus.length, self.map_w)):
                if is_vehicle(self.cars[x_ind+i][y_ind]):
                    car = self.cars[x_ind+i][y_ind]
                    dist = i
                    return dist > car.length
            return False

    def spawn_cars(self):
        # Budryka & Kawiory
        prob_budryka_spawn = Fraction(14, 1000)
        if rand_with_probability(prob_budryka_spawn):
            car_scooter_prob = Fraction(10, 13)
            initial_pos = (669, 70)
            if rand_with_probability(car_scooter_prob):
                veh = Car(initial_pos, self.cars)
            else:
                veh = Scooter(initial_pos, self.cars)
            self.budryka_cars[1].append(veh)
        prob_kawiory_spawn = Fraction(1, 300)
        if rand_with_probability(prob_kawiory_spawn):
            car_scooter_prob = Fraction(2, 3)
            initial_pos = (751, 70)
            if rand_with_probability(car_scooter_prob):
                veh = Car(initial_pos, self.cars)
            else:
                veh = Scooter(initial_pos, self.cars)
            self.kawiory_cars[1].append(veh)
        # Kijowska
        phase = self.iter_counter % 60
        initial_pos = (self.map_w-1, 15)
        if 40 > phase >= 0 and not self.is_occupied(initial_pos[0], initial_pos[1]):
            prob_kijowska_spawn = Fraction(1, 15)
            if rand_with_probability(prob_kijowska_spawn):
                self.add_car(Car(initial_pos, self.cars))
        elif phase == 40:
            cars_to_spawn = randint(7, 13)
            for i in range(cars_to_spawn):
                rand = randint(1, 149)
                if rand < 143:
                    self.kijowska_to_spawn.put(Car(initial_pos, self.cars))
                elif rand < 147:
                    self.kijowska_to_spawn.put(BigBus(initial_pos, self.cars))
                elif rand < 149:
                    self.kijowska_to_spawn.put(Bus(initial_pos, self.cars))
                else:
                    self.kijowska_to_spawn.put(Truck(initial_pos, self.cars))
        elif not self.kijowska_to_spawn.empty() and not self.is_occupied(initial_pos[0], initial_pos[1]):
            self.add_car(self.kijowska_to_spawn.get())
        # Armii Krajowej
        initial_pos = (0, 33)
        phase = self.iter_counter % 120
        if phase == 0:
            cars_to_spawn = randint(13, 19)
            for i in range(cars_to_spawn):
                rand = randint(1, 153)
                if rand < 133:
                    self.ak_to_spawn.put(Car(initial_pos, self.cars))
                elif rand < 141:
                    self.ak_to_spawn.put(BigBus(initial_pos, self.cars))
                elif rand < 147:
                    self.ak_to_spawn.put(Bus(initial_pos, self.cars))
                elif rand < 153:
                    self.ak_to_spawn.put(Scooter(initial_pos, self.cars))
                else:
                    self.ak_to_spawn.put(Truck(initial_pos, self.cars))
        elif phase < 50:
            if not self.is_occupied(initial_pos[0], initial_pos[1]):
                self.add_car(self.ak_to_spawn.get())
        elif not self.is_occupied(initial_pos[0], initial_pos[1]):
            prob_piastowska_spawn = Fraction(2, 35)
            if rand_with_probability(prob_piastowska_spawn):
                self.add_car(Car(initial_pos, self.cars))

    def traffic_lights_crossing(self):
        # stale (ilosc iteracji po ktorych nastepuje zmiana)
        crossing_open_duration = 40
        crossing_close_duration = 20

        if self.crossing_closed is False and \
            self.iter_counter % (crossing_close_duration + crossing_open_duration) == 0:
            self.crossing_closed = True
            for i in range(229, 255):
                for j in range(14, 34):
                    if self.map[i][j] == 3:  # crossing
                        self.map[i][j] = 6  # crossing_close

        if self.crossing_closed is True and self.iter_counter % (
                crossing_close_duration + crossing_open_duration) == crossing_open_duration:
            self.crossing_closed = False
            for i in range(229, 255):
                for j in range(14, 34):
                    if self.map[i][j] == 6:  # crossing_close
                        self.map[i][j] = 3  # crossing

    def iteration(self):
        self.spawn_cars()
        self.traffic_lights_crossing()
        self.spawn_pedestrians()
        self.move_pedestrians()
        self.move_cars()
        self.iter_counter += 1

    def move_cars(self):
        cars_copy = copy.deepcopy(self.cars)
        for x in range(self.map_w):
            for y in range(len(cars_copy[x])):
                if is_vehicle(cars_copy[x][y]):
                    self.cars[x][y].set_speed()
        for x in range(self.map_w):
            if is_vehicle(cars_copy[x][0]):
                new_x = x - self.cars[x][0].speed
                if new_x >= 0:
                    self.move_car(x, 0, new_x, 0)
                self.cars[x][0] = 0
            if is_vehicle(cars_copy[x][1]):
                new_x = x + self.cars[x][1].speed
                if new_x < self.map_w:
                    if self.cars[new_x][1] is not None:
                        self.move_car(x, 1, new_x, 1)
                    else:
                        self.move_car(x, 1, new_x, 2)
                else:
                    self.cars[x][1] = 0
            if is_vehicle(cars_copy[x][2]):
                new_x = x + self.cars[x][2].speed
                if new_x < self.map_w:
                    self.move_car(x, 2, new_x, 2)
                else:
                    self.cars[x][2] = 0

    def move_car(self, x_from, y_from, x_to, y_to):
        if x_to == x_from and y_from == y_to:
            return
        if is_vehicle(self.cars[x_to][y_to]):
            raise Exception("2 cars cannot be on one field")
        if y_to == y_from:
            self.cars[x_from][y_from].position = (x_to, self.cars[x_from][y_to].position[1])
        elif y_to == 2:
            self.cars[x_from][y_from].position = (x_to, 33)
        elif y_to == 1:
            self.cars[x_from][y_from].position = (x_to, 27)
        elif y_to == 0:
            self.cars[x_from][y_from].position = (x_to, 15)
        else:
            print("Unknown position")
        self.cars[x_to][y_to] = self.cars[x_from][y_from]
        self.cars[x_from][y_from] = 0

    def spawn_pedestrians(self):

        for area in self.pedestrian_areas:
            if area.type == 1 and not self.crossing_closed:
                continue
            if randint(0, 100) <= area.spawn_prob:
                if randint(1, 2) == 1:
                    area.spawn_pedestrian_up()
                else:
                    area.spawn_pedestrian_down()

    def move_pedestrians(self):

        for area in self.pedestrian_areas:
            if area.type == 1 and self.crossing_closed:
                continue
            area.iterate()

    def add_car(self, vehicle):
        pos = map_pos_to_arr_ind(vehicle.position)
        self.cars[pos[0]][pos[1]] = vehicle

