import pygame
import pygame_menu
import sys

# gui params init
size = width, height = 1200, 210
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
screen = pygame.display.set_mode(size)

# main loop
while True:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # moving screen with arrows
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and scroll_x < 0:
        scroll_x += scroll_vel
    if keys[pygame.K_RIGHT] and scroll_x > -988:
        scroll_x -= scroll_vel

    # map drawing
    for i in range(map_w + 1):
        for j in range(map_h + 1):
            pygame.draw.rect(screen, colors[map[i][j]],
                             pygame.Rect((i + scroll_x) * cell_size, j * cell_size, cell_size, cell_size))

    pygame.display.flip()
