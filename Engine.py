from collections import namedtuple
import queue
from random import randint
from Participants import *

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

    def __init__(self, map: list):
        self.map_w = len(map)
        self.map_h = len(map[0])
        self.map = map
        self.crossing_closed = False
        self.iter_counter = 0
        self.budryka_cars = [[], []]
        self.kawiory_cars = [[], []]
        self.kijowska_to_spawn = queue.Queue()
        self.ak_to_spawn = queue.Queue()

    def get_map(self):  # todo
        return [[0 for _ in range(self.map_h)] for i in range(self.map_w)]

    def is_occupied(self, x: int, y: int) -> bool:  # todo
        if self.map[x][y] == 4 or self.map[x][y] == 5:
            return False

        return True

    def spawn_cars(self):  # todo
        # Budryka & Kawiory
        prob_budryka_spawn = Fraction(14, 1000)
        if rand_with_probability(prob_budryka_spawn):
            car_scooter_prob = Fraction(10, 13)
            initial_pos = (669, 70)
            if rand_with_probability(car_scooter_prob):
                veh = Car(initial_pos)
            else:
                veh = Scooter(initial_pos)
            self.budryka_cars[1].append(veh)
        prob_kawiory_spawn = Fraction(1, 300)
        if rand_with_probability(prob_kawiory_spawn):
            car_scooter_prob = Fraction(2, 3)
            initial_pos = (751, 70)
            if rand_with_probability(car_scooter_prob):
                veh = Car(initial_pos)
            else:
                veh = Scooter(initial_pos)
            self.kawiory_cars[1].append(veh)
        # Kijowska
        phase = self.iter_counter % 60
        initial_pos = (1390, 15)
        if 40 > phase >= 0 and not self.is_occupied(initial_pos[0], initial_pos[1]):
            prob_kijowska_spawn = Fraction(1, 15)
            if rand_with_probability(prob_kijowska_spawn):
                self.add_car(Car(initial_pos))
        elif phase == 40:
            cars_to_spawn = randint(7, 13)
            for i in range(cars_to_spawn):
                rand = randint(1, 149)
                if rand < 143:
                    self.kijowska_to_spawn.put(Car(initial_pos))
                elif rand < 147:
                    self.kijowska_to_spawn.put(BigBus(initial_pos))
                elif rand < 149:
                    self.kijowska_to_spawn.put(Bus(initial_pos))
                else:
                    self.kijowska_to_spawn.put(Truck(initial_pos))
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
                    self.ak_to_spawn.put(Car(initial_pos))
                elif rand < 141:
                    self.ak_to_spawn.put(BigBus(initial_pos))
                elif rand < 147:
                    self.ak_to_spawn.put(Bus(initial_pos))
                elif rand < 153:
                    self.ak_to_spawn.put(Scooter(initial_pos))
                else:
                    self.ak_to_spawn.put(Truck(initial_pos))
        elif phase < 50:
            if not self.is_occupied(initial_pos[0], initial_pos[1]):
                self.add_car(self.ak_to_spawn.get())
        elif not self.is_occupied(initial_pos[0], initial_pos[1]):
            prob_piastowska_spawn = Fraction(2, 35)
            if rand_with_probability(prob_piastowska_spawn):
                self.add_car(Car(initial_pos))

    def traffic_lights_crossing(self):
        # stale (ilosc iteracji po ktorych nastepuje zmiana)
        crossing_open_duration = 40
        crossing_close_duration = 10

        if self.crossing_closed is False and self.iter_counter % (
                crossing_close_duration + crossing_open_duration) == crossing_open_duration:
            self.crossing_closed = True
            for i in range(229, 255):
                for j in range(14, 34):
                    if self.map[i][j] == 3:  # crossing
                        self.map[i][j] = 6  # crossing_close

        if self.crossing_closed is True and self.iter_counter % (crossing_close_duration + crossing_open_duration) == 0:
            self.crossing_closed = False
            for i in range(229, 255):
                for j in range(14, 34):
                    if self.map[i][j] == 6:  # crossing_close
                        self.map[i][j] = 3  # crossing
        # todo jak juz bedzie tablica ta 3x1400 dopisac aby tam przestawiał sie czynnik open w crossign

    def iteration(self):  # todo
        # self.spawn_cars()
        self.traffic_lights_crossing()

        # 3x1400
        self.iter_counter += 1

    def move_cars(self):  # todo
        pass

    def spawn_pedestrians(self):  # todo
        pass

    def move_pedestrians(self):  # todo
        pass

    def add_car(self, vehicle):
        pass
