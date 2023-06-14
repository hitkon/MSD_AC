from collections import namedtuple

Fraction = namedtuple('Fraction', ['numerator', 'denominator'])


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

    def iteration(self):    # todo
        self.spawn_cars()

    def get_map(self):      # todo
        return [[0 for _ in range(self.map_h)] for i in range(self.map_w)]

    def is_occupied(self, x: int, y: int):    # todo
        return True

    def spawn_cars(self):                     # todo
        if not self.is_occupied(0, 1):
            pass

    def move_cars(self):                      # todo
        pass

    def spawn_pedestrians(self):              # todo
        pass

    def move_pedestrians(self):               # todo
        pass
