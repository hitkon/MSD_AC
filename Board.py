import pygame
import pygame_menu
import sys

class Board:
    # gui params
    main_window_size = main_window_width, main_window_height = 1200, 420
    sub_window_size = sub_window_width, sub_window_height = 1200, 210
    speed = [1, 1]
    black = 0, 0, 0
    cell_size = 3
    scroll_x = 0
    scroll_vel = 4
    main_screen = None
    sub_screen = None
    legend_elems = []
    legend_labels = ["Legend:", "Pavement", "Road", "Crossing", "Vehicle", "Pedestrian"]

    # map params
    map = []
    map_h, map_w = 0, 0
    # colors_ids: 0 - not usable, 1 - pavement, 2 - road, 3 - crossing, 4 - vehicle, 5 - pedestrian
    colors = [(255, 255, 255), (155, 155, 155), (0, 0, 102), (0, 102, 51), (255, 255, 102), (0, 0, 0)]

    def __init__(self, cell_size=3, scroll_vel=4, legend_font_size=30):
        pygame.init()
        self.cell_size = cell_size
        self.scroll_vel = scroll_vel
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, legend_font_size)
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
        # descriptions
        counter = 10
        for label in self.legend_labels:
            self.legend_elems.append(self.font.render(label, True, (0, 0, 0)))
            self.sub_screen.blit(self.legend_elems[-1], (10, counter))
            counter += 30
        # colored squares
        for i in range(1, len(self.legend_elems)):
            pygame.draw.rect(self.sub_screen, self.colors[i], pygame.Rect(150, 10 + 30*i, 20, 20))

    def is_click_inside_scrollbar(self, event):
        return event.pos[0] >= self.scrollbar_x and event.pos[
            0] <= self.scrollbar_x + self.scrollbar_width and self.main_window_height - self.scrollbar_height <= \
            event.pos[1] and self.main_window_height >= event.pos[1]

    def start(self):
        self.init_map()
        self.main_screen = pygame.display.set_mode(self.main_window_size)
        self.sub_screen = pygame.Surface(self.sub_window_size)
        self.sub_screen.fill((255, 255, 255))
        self.create_legend()

        #self.total_width = self.map_w * self.cell_size
        self.total_width = 2150
        # self.scrollbar_width = self.total_width /
        self.scrollbar_mult = (self.total_width - self.main_window_width) / (
                    self.main_window_width - self.scrollbar_width)

        self.main_loop()


    def main_loop(self):
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


            # moving screen with arrows
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.scroll_x < 0:
                self.scroll_x += self.scroll_vel
            if keys[pygame.K_RIGHT] and self.scroll_x > -988:
                self.scroll_x -= self.scroll_vel
            # map drawing on the main screen
            self.main_screen.fill((0, 0, 0))
            for i in range(self.map_w + 1):
                for j in range(self.map_h + 1):
                    pygame.draw.rect(self.main_screen, self.colors[self.map[i][j]],
                                     pygame.Rect((i + self.scroll_x) * self.cell_size, j * self.cell_size,
                                                 self.cell_size, self.cell_size))

            # drawing subscreen with legend
            self.main_screen.blit(self.sub_screen, ((self.main_window_width - self.sub_window_width) // 2,
                                                    self.main_window_height - self.sub_window_height))
            pygame.draw.rect(self.main_screen, (0, 0, 0), pygame.Rect(self.scrollbar_x,
                                                                      self.main_window_height - self.scrollbar_height,
                                                                      self.scrollbar_width,
                                                                      self.scrollbar_height))
            # todo figure out how to draw legend only once
            pygame.display.flip()

if __name__ == '__main__':
    my_board = Board()
    my_board.start()
