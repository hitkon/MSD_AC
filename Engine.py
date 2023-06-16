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

    def __init__(self, map_h: int, map_w: int):
        self.map_h = map_h
        self.map_w = map_w
        self.iter_counter = 0
        self.budryka_cars = [[], []]
        self.kawiory_cars = [[], []]

    def iteration(self):    # todo
        self.spawn_cars()
        self.iter_counter += 1

    def get_map(self):      # todo
        return [[0 for _ in range(self.map_h)] for i in range(self.map_w)]

    def is_occupied(self, x: int, y: int):    # todo
        return True

    def spawn_cars(self):                     # todo
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

    def move_cars(self):                      # todo
        pass

    def spawn_pedestrians(self):              # todo
        pass

    def move_pedestrians(self):               # todo
        pass
