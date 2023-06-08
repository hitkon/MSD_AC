import pygame
import pygame_menu
import sys

# gui params init
main_window_size = main_window_width, main_window_height = 1200, 420
sub_window_size = sub_window_width, sub_window_height = 1200, 210
speed = [1, 1]
black = 0, 0, 0
cell_size = 3
scroll_x = 0
scroll_vel = 4
clock = pygame.time.Clock()

pygame.init()
# colors_ids: 0 - not usable, 1 - pavement, 2 - road, 3 - crossing, 4 - vehicle, 5 - pedestrian
colors = [(255, 255, 255), (155, 155, 155), (0, 0, 102), (0, 102, 51), (255, 255, 102), (0, 0, 0)]

# map initialization
map_h, map_w = 0, 0
map = []
with open("map/map0", "r") as f:
    w, h, n = [int(x) for x in next(f).split()]
    map_h, map_w = h, w
    for _ in range(w + 1):
        map.append([0 for _ in range(h + 1)])
    for _ in range(n):
        x0, y0, x1, y1, t = [int(x) for x in next(f).split()]
        for i in range(x0, x1+1):
            for j in range(y0, y1+1):
                map[i][j] = t

print(map)           # debugging purposes
main_screen = pygame.display.set_mode(main_window_size)

# Tworzenie drugiego okna
sub_screen = pygame.Surface(sub_window_size)
sub_screen.fill((255, 255, 255))


font = pygame.font.Font(None, 36)

# legenda opisy
legend_title = font.render("Legend:", True, (0, 0, 0))
pavement_legend = font.render("Pavement", True, (0, 0, 0))
road_legend = font.render("Road", True, (0, 0, 0))
crossing_legend = font.render("Crossing", True, (0, 0, 0))
vehicle_legend = font.render("Vehicle", True, (0, 0, 0))
pedestrian_legend = font.render("Pedestrian", True, (0, 0, 0))

sub_screen.blit(legend_title, (10, 10))
sub_screen.blit(pavement_legend, (10, 40))
sub_screen.blit(road_legend, (10, 70))
sub_screen.blit(crossing_legend, (10, 100))
sub_screen.blit(vehicle_legend, (10, 130))
sub_screen.blit(pedestrian_legend, (10, 160))

# kolorowe kwadraty
pygame.draw.rect(sub_screen, colors[1], pygame.Rect(180, 40, 20, 20))
pygame.draw.rect(sub_screen, colors[2], pygame.Rect(180, 70, 20, 20))
pygame.draw.rect(sub_screen, colors[3], pygame.Rect(180, 100, 20, 20))
pygame.draw.rect(sub_screen, colors[4], pygame.Rect(180, 130, 20, 20))
pygame.draw.rect(sub_screen, colors[5], pygame.Rect(180, 160, 20, 20))

# main loop
while True:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # moving screen with arrows
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and scroll_x < 0:
        scroll_x += scroll_vel
    if keys[pygame.K_RIGHT] and scroll_x > -988:
        scroll_x -= scroll_vel

    # map drawing on the main screen
    main_screen.fill((0, 0, 0))
    for i in range(map_w + 1):
        for j in range(map_h + 1):
            pygame.draw.rect(main_screen, colors[map[i][j]],
                             pygame.Rect((i + scroll_x) * cell_size, j * cell_size, cell_size, cell_size))

    # Rysowanie drugiego okna na głównym ekranie
    main_screen.blit(sub_screen, ((main_window_width - sub_window_width) // 2, main_window_height - sub_window_height))

    pygame.display.flip()
