from random import randint
import copy
from Participants import Pedestrian


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

        x = randint(0, self.total_width - 1)
        y = randint(self.up_spawn_range[0], self.up_spawn_range[1]) - self.up_spawn_range[0]
        # while len(self.map[x][y]) != 0:
        #     x = randint(0, self.total_width - 1)
        #     y = randint(self.up_spawn_range[0], self.up_spawn_range[1]) - self.up_spawn_range[0]
        self.map[x][y].append(Pedestrian((x, y), -1))

    def spawn_pedestrian_down(self):

        x = randint(0, self.total_width - 1)
        y = randint(self.down_spawn_range[0], self.down_spawn_range[1]) - self.up_spawn_range[0]
        # while len(self.map[x][y]) != 0:
        #     x = randint(0, self.total_width - 1)
        #     y = randint(self.down_spawn_range[0], self.down_spawn_range[1]) - self.up_spawn_range[0]
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

    def is_anyone_at_crossing(self):
        for i in range(self.total_width):
            for j in range(self.total_height):
                if len(self.map[i][j]) != 0:
                    return True
        return False

    def iterate(self):
        self.update_speed()
        self.move()


class Crossing:
    """
    obiekt - przejscie dla pieszych, ustawia sie w nim czy przejscie jest otwrte czy zamkanięte
    (open == true -> auto moze jechac)

    Prawdopodobnie zamienic na obiekty klasy PedastrainCrossing
    """

    def __init__(self, position: (int, int), open: bool):
        self.position = position
        self.open = open
