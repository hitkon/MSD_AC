import pygame
import pygame_menu
import sys

# gui params init
size = width, height = 800, 490
speed = [1, 1]
black = 0, 0, 0
cell_size = 7
scroll_x = 0
scroll_vel = 1
clock = pygame.time.Clock()

#border_size = 2
pygame.init()
# colors_ids: 0 - not usable, 1 - pedestrian road, 2 - road, 3 - crossing, 4 - vehicle , 5-pedestrian
colors = [(255, 255, 255), (155, 155, 155), (0, 0, 102), (0, 102, 51), (255, 255, 102), (0, 0, 0)]

# map initialization
map_h, map_w = 0, 0
map = []
with open("map/map0", "r") as f:
    h, w, n = [int(x) for x in next(f).split()]
    map_w, map_h = w, h
    for _ in range(h+1):
        map.append([0 for _ in range(w+1)])
    for _ in range(n):
        x0, y0, x1, y1, t = [int(x) for x in next(f).split()]
        for i in range(x0, x1+1):
            for j in range(y0, y1+1):
                map[i][j] = t

print(map)           # debugging purposes
screen = pygame.display.set_mode(size)

# todo fill in what this section does
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
print(ball.get_rect())       # debugging purposes

# main loop
while True:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
    #screen.fill(black)

    # moving screen with arrows
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and scroll_x < map_w:
        scroll_x += scroll_vel
    if keys[pygame.K_RIGHT] and scroll_x > 0:
        scroll_x -= scroll_vel

    # map drawing
    for i in range(map_h+1):
        for j in range(map_w+1):
            pygame.draw.rect(screen, colors[map[i][j]],
                             pygame.Rect(i * cell_size + scroll_x, j * cell_size, cell_size, cell_size))

    # ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]


    # screen.blit(ball, ballrect)
    pygame.display.flip()
