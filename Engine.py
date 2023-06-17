from collections import namedtuple
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
        self.map_w = len(map) - 1
        self.map_h = len(map[0]) - 1
        self.map = map
        self.crossing_closed = False
        self.iter_counter = 0
        self.budryka_cars = [[], []]
        self.kawiory_cars = [[], []]

    def get_map(self):  # todo
        return [[0 for _ in range(self.map_h)] for i in range(self.map_w)]

    def is_occupied(self, x: int, y: int):  # todo
        return True

    def spawn_cars(self):  # todo
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
        if not self.is_occupied(0, 1):
            pass

    def traffic_lights_crossing(self):
        # stale (ilosc iteracji po ktorych nastepuje zmiana)
        crossing_open_duration = 40
        crossing_close_duration = 20

        if self.crossing_closed is False and self.iter_counter % crossing_open_duration == 0:
            self.crossing_closed = True
            for i in range(self.map_w + 1):
                for j in range(self.map_h + 1):
                    if i < 300:
                        if self.map[i][j] == 3:  # crossing
                            self.map[i][j] = 6  # crossing_close

        if self.crossing_closed is True and self.iter_counter % (
                crossing_open_duration + crossing_close_duration) == crossing_open_duration:
            self.crossing_closed = False
            for i in range(self.map_w + 1):
                for j in range(self.map_h + 1):
                    if i < 300:
                        if self.map[i][j] == 6:  # crossing_close
                            self.map[i][j] = 3  # crossing

    def iteration(self):  # todo
        # self.spawn_cars()
        self.traffic_lights_crossing()
        self.iter_counter += 1

    def move_cars(self):  # todo
        pass

    def spawn_pedestrians(self):  # todo
        pass

    def move_pedestrians(self):  # todo
        pass
