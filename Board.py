import pygame
import sys

class Board:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.main_window_size = self.main_window_width, self.main_window_height = 1200, 420
        self.sub_window_size = self.sub_window_width, self.sub_window_height = 1200, 210
        self.speed = [1, 1]
        self.black = 0, 0, 0
        self.cell_size = 3
        self.scroll_x = 0
        self.scroll_vel = 4
        self.main_screen = None
        self.sub_screen = None
        self.legend_elems = []
        self.legend_labels = ["Legend:", "Pavement", "Road", "Crossing", "Vehicle", "Pedestrian", "Crossing closed"]
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
        counter = 10
        for label in self.legend_labels:
            self.legend_elems.append(self.font.render(label, True, (0, 0, 0)))
            self.sub_screen.blit(self.legend_elems[-1], (10, counter))
            counter += 30
        for i in range(1, len(self.legend_elems)):
            pygame.draw.rect(self.sub_screen, self.colors[i], pygame.Rect(150, 10 + 30 * i, 20, 20))

    def is_click_inside_scrollbar(self, event):
        return (
            event.pos[0] >= self.scrollbar_x and event.pos[0] <= self.scrollbar_x + self.scrollbar_width and
            self.main_window_height - self.scrollbar_height <= event.pos[1] and self.main_window_height >= event.pos[1]
        )

    def start(self):
        self.init_map()
        self.main_screen = pygame.display.set_mode(self.main_window_size)
        self.sub_screen = pygame.Surface(self.sub_window_size)
        self.sub_screen.fill((255, 255, 255))
        self.create_legend()
        self.total_width = 2150
        self.scrollbar_mult = (self.total_width - self.main_window_width) / (self.main_window_width - self.scrollbar_width)
        self.main_loop()

    def main_loop(self):
        crossing_closed = False
        crossing_duration = 40000
        crossing_close_duration = 20000
        crossing_start_time = pygame.time.get_ticks()

        while True:
            self.clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.is_click_inside_scrollbar(event):
                        self.scrollbar_pressed = True
                        print(event.pos[0], event.pos[1])
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.scrollbar_pressed = False
                if event.type == pygame.MOUSEMOTION:
                    if self.scrollbar_pressed:
                        self.scrollbar_x += event.rel[0]
                        self.scrollbar_x = max(0, self.scrollbar_x)
                        self.scrollbar_x = min(self.main_window_width - self.scrollbar_width, self.scrollbar_x)
                        self.scroll_x = - self.scrollbar_x * self.scrollbar_mult

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.scroll_x < 0:
                self.scroll_x += self.scroll_vel
            if keys[pygame.K_RIGHT] and self.scroll_x > -988:
                self.scroll_x -= self.scroll_vel

            self.main_screen.fill((0, 0, 0))
            for i in range(self.map_w + 1):
                for j in range(self.map_h + 1):
                    pygame.draw.rect(
                        self.main_screen, self.colors[self.map[i][j]],
                        pygame.Rect((i + self.scroll_x) * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    )

            self.main_screen.blit(
                self.sub_screen, ((self.main_window_width - self.sub_window_width) // 2, self.main_window_height - self.sub_window_height)
            )
            pygame.draw.rect(
                self.main_screen, (0, 0, 0),
                pygame.Rect(self.scrollbar_x, self.main_window_height - self.scrollbar_height, self.scrollbar_width, self.scrollbar_height)
            )
            pygame.display.flip()

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - crossing_start_time

            if crossing_closed == False and elapsed_time >= crossing_duration:
                crossing_closed = True
                crossing_start_time = current_time
                for i in range(self.map_w + 1):
                    for j in range(self.map_h + 1):
                        if i < 300:
                            if self.map[i][j] == 3:  # crossing
                                self.map[i][j] = 6  # crossing_close
            elif crossing_closed == True and elapsed_time >= crossing_close_duration:
                crossing_closed = False
                crossing_start_time = current_time
                for i in range(self.map_w + 1):
                    for j in range(self.map_h + 1):
                        if i < 300:
                            if self.map[i][j] == 6:  # crossing_close
                                self.map[i][j] = 3  # crossing


if __name__ == '__main__':
    my_board = Board()
    my_board.start()
