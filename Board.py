import pygame
import sys
import Engine


class Board:
    def __init__(self):
        self.pedestrian_areas = []
        self.total_width = None
        pygame.init()
        self.clock = pygame.time.Clock()
        self.main_window_size = self.main_window_width, self.main_window_height = 1200, 420
        self.sub_window_size = self.sub_window_width, self.sub_window_height = 1200, 210
        self.speed = [1, 1]
        self.cell_size = 3
        self.scroll_x = 0
        self.scroll_vel = 4
        self.main_screen = None
        self.sub_screen = None
        self.legend_elems = []
        self.legend_labels = ["Legend:", "Pavement", "Road", "Crossing", "Vehicle", "Pedestrian", "Crossing closed"]
        self.speed_cont_vals = [1, 2, 3, 4, 5, 10, 25, 50, 100]
        self.chosen_speed = 0   # index of array above
        self.speed_cont_x = 600
        self.speed_box_width = 15
        self.map = []
        self.map_h, self.map_w = 0, 0
        # colors_ids: 0 - not usable, 1 - pavement, 2 - road, 3 - crossing, 4 - vehicle, 5 - pedestrian, 6 - crossing_closed
        self.colors = [(255, 255, 255), (155, 155, 155), (0, 0, 102), (0, 102, 51), (255, 255, 102), (0, 0, 0), (255, 0, 0)]
        self.cell_size = 3
        self.scroll_vel = 4
        self.font = pygame.font.Font(None, 30)
        self.scrollbar_x = 0
        self.scrollbar_width = 100
        self.scrollbar_height = 20
        self.scrollbar_pressed = False
        self.scrollbar_mult = 0
        self.engine = None

    def load_pedestrian_spawn_points(self):
        with open("map/people_spawn_points0.txt") as f:
            n = int(f.readline())
            for _ in range(n):
                args = f.readline().split(" ")
                crossing = Engine.PedestrianCrossing(width_range=(int(args[0]), int(args[1])),
                                                     up_spawn_range=(int(args[2]), int(args[3])),
                                                     down_spawn_range=(int(args[4]), int(args[5])),
                                                     type=int(args[6]),
                                                     spawn_prob=int(args[7]))
                self.pedestrian_areas.append(crossing)

    def init_map(self):
        with open("map/map0", "r") as f:
            w, h, n = [int(x) for x in next(f).split()]
            self.map_h, self.map_w = h, w
            for _ in range(w + 1):
                self.map.append([0 for _ in range(h + 1)])
            for _ in range(n):
                x0, y0, x1, y1, t = [int(x) for x in next(f).split()]
                for i in range(x0, x1 + 1):
                    for j in range(y0, y1 + 1):
                        self.map[i][j] = t

    def create_legend(self):
        spacing = 270
        elems_in_col = 5
        counter = [10, 10]
        for label in self.legend_labels:
            self.legend_elems.append(self.font.render(label, True, (0, 0, 0)))
            self.sub_screen.blit(self.legend_elems[-1], counter)
            counter[1] += 30
            if counter[1] > (elems_in_col+1)*30:
                counter[0] += spacing
                counter[1] = 40
        for i in range(1, len(self.legend_elems)):
            pygame.draw.rect(self.sub_screen, self.colors[i], pygame.Rect(180 + spacing*((i-1)//elems_in_col),
                                                                          40 + 30 * ((i-1) % elems_in_col), 20, 20))

    def create_speed_control(self):
        self.sub_screen.blit(self.font.render("Simulation speed", True, (0, 0, 0)), [self.speed_cont_x, 10])
        counter = self.speed_cont_x
        for i in self.speed_cont_vals:
            self.sub_screen.blit(self.font.render(str(i), True, (0, 0, 0)), [counter, 70])
            counter += 30

    def is_click_inside_scrollbar(self, event):
        return (
                self.scrollbar_x <= event.pos[0] <= self.scrollbar_x + self.scrollbar_width and
                self.main_window_height - self.scrollbar_height <= event.pos[1] <= self.main_window_height
        )

    def is_click_in_counters_zone(self, event):
        n = len(self.speed_cont_vals)
        return self.speed_cont_x <= event.pos[0] <= self.speed_cont_x + n*(n-1)*self.speed_box_width \
            and self.sub_window_size[1] + 40 <= event.pos[1] <= self.sub_window_size[1] + 40 + self.speed_box_width \
            and (event.pos[0] - self.speed_cont_x)//self.speed_box_width % 2 == 0

    def start(self):
        self.init_map()
        self.load_pedestrian_spawn_points()
        self.engine = Engine.Engine(self.map, self.pedestrian_areas)
        Engine.RoadVehicle.engine = self.engine
        self.main_screen = pygame.display.set_mode(self.main_window_size)
        self.sub_screen = pygame.Surface(self.sub_window_size)
        self.sub_screen.fill((255, 255, 255))
        self.create_legend()
        self.create_speed_control()
        #self.total_width = self.map_w * self.cell_size
        self.total_width = 2190
        # self.scrollbar_width = self.total_width /
        self.scrollbar_mult = (self.total_width - self.main_window_width) / (
                    self.main_window_width - self.scrollbar_width)
        self.main_loop()

    def draw_pedestrians(self):
        for area in self.pedestrian_areas:
            for i in range(area.total_width):
                for j in range(area.total_height):
                    if len(area.map[i][j]) != 0:
                        pygame.draw.rect(
                            self.main_screen, self.colors[5],
                            pygame.Rect((i + area.width_range[0] + self.scroll_x) * self.cell_size,
                                        (j + area.up_spawn_range[0]) * self.cell_size, self.cell_size,
                                        self.cell_size)
                        )

    def change_simulation_speed(self, event):
        i = (event.pos[0] - self.speed_cont_x)//self.speed_box_width
        self.chosen_speed = i//2

    def draw_cars(self):
        cars = self.engine.cars
        for i in range(len(cars)):
            for j in range(len(cars[i])):
                if isinstance(cars[i][j], Engine.RoadVehicle):
                    x_be, y_be = cars[i][j].position
                    drawing_range = (cars[i][j].length, cars[i][j].width)
                    if j != 0:
                        x_be = x_be - drawing_range[0]
                        y_be = y_be - drawing_range[1]
                    pygame.draw.rect(self.main_screen, self.colors[4],
                                     pygame.Rect((x_be + self.scroll_x)*self.cell_size, y_be*self.cell_size,
                                                 drawing_range[0]*self.cell_size, drawing_range[1]*self.cell_size))

        def draw_cars_from_list(cars: list, upwards: bool):
            for car in cars:
                x_be, y_be = car.position
                drawing_range = (car.width, car.length)
                if upwards:
                    x_be -= drawing_range[0]
                else:
                    y_be -= drawing_range[1]
                pygame.draw.rect(self.main_screen, self.colors[4],
                                 pygame.Rect((x_be + self.scroll_x) * self.cell_size, y_be * self.cell_size,
                                             drawing_range[0] * self.cell_size, drawing_range[1] * self.cell_size))

        draw_cars_from_list(self.engine.budryka_cars[0], False)
        draw_cars_from_list(self.engine.budryka_cars[1], True)
        draw_cars_from_list(self.engine.kawiory_cars[0], False)
        draw_cars_from_list(self.engine.kawiory_cars[1], True)

    def draw_map(self):
        self.main_screen.fill((0, 0, 0))
        for i in range(self.map_w + 1):
            for j in range(self.map_h + 1):
                pygame.draw.rect(
                    self.main_screen, self.colors[self.map[i][j]],
                    pygame.Rect((i + self.scroll_x) * self.cell_size, j * self.cell_size, self.cell_size,
                                self.cell_size)
                )

    def draw_scrollbar(self):
        self.main_screen.blit(
            self.sub_screen,
            ((self.main_window_width - self.sub_window_width) // 2, self.main_window_height - self.sub_window_height)
        )
        pygame.draw.rect(
            self.main_screen, (0, 0, 0),
            pygame.Rect(self.scrollbar_x, self.main_window_height - self.scrollbar_height, self.scrollbar_width,
                        self.scrollbar_height)
        )

    def draw_speed_control(self):
        x_pos = self.speed_cont_x
        y_pos = 40
        width = self.speed_box_width
        contour = 3
        button_col = (255, 0, 0)
        for i in range(len(self.speed_cont_vals)):
            pygame.draw.rect(self.sub_screen, button_col, pygame.Rect(x_pos, y_pos, width, width))
            pygame.draw.rect(self.sub_screen, (255, 255, 255), pygame.Rect(x_pos + contour, y_pos + contour,
                                                                           width - 2*contour, width - 2*contour))
            if self.chosen_speed == i:
                pygame.draw.rect(self.sub_screen, button_col, pygame.Rect(x_pos + contour + 1, y_pos + contour + 1,
                                                                               width - 2 * (contour + 1),
                                                                               width - 2 * (contour + 1)))
            x_pos += 2*width

    def main_loop(self):
        # clock = pygame.time.Clock()
        # iteration_interval = 500  # Czas w milisekundach między iteracjami (1 sekunda = 1000 milisekund)
        iteration_interval = 1000  # Time between iterations in ms
        elapsed_time = 0
        while True:
            delta_time = self.clock.tick()
            elapsed_time += delta_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos[0], event.pos[1])
                    if event.button == 1 and self.is_click_inside_scrollbar(event):
                        self.scrollbar_pressed = True
                        #print(event.pos[0], event.pos[1])
                    elif event.button == 1 and self.is_click_in_counters_zone(event):
                        self.change_simulation_speed(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.scrollbar_pressed = False
                if event.type == pygame.MOUSEMOTION:
                    if self.scrollbar_pressed:
                        self.scrollbar_x += event.rel[0]
                        self.scrollbar_x = max(0, self.scrollbar_x)
                        self.scrollbar_x = min(self.main_window_width - self.scrollbar_width, self.scrollbar_x)
                        self.scroll_x = - self.scrollbar_x * self.scrollbar_mult

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT] and self.scroll_x < 0:
            #     self.scroll_x += self.scroll_vel
            # if keys[pygame.K_RIGHT] and self.scroll_x > -988:
            #     self.scroll_x -= self.scroll_vel              # arrows movement

            self.draw_map()
            self.draw_scrollbar()
            self.draw_speed_control()
            self.draw_pedestrians()
            self.draw_cars()
            if elapsed_time >= iteration_interval//self.speed_cont_vals[self.chosen_speed]:
                self.engine.iteration()
                elapsed_time = 0
            pygame.display.flip()


if __name__ == '__main__':
    my_board = Board()
    my_board.start()
