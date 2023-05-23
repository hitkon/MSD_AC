import sys, pygame, pygame_menu

size = width, height = 800, 490
speed = [1, 1]
black = 0, 0, 0
cell_size = 7
#border_size = 2
pygame.init()
# colors_ids: 0 - not usable, 1 - pedestrian road, 2 - road, 3-przejscie, 4-auto , 5-pedestrian
colors = [(255, 255, 255), (155, 155, 155), (0,0,102), (0, 102, 51), (255,255,102), (0,0,0)]
map_h, map_w = 0,0
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

print (map)
screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
print(ball.get_rect())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    #screen.fill(black)
    for i in range(map_h+1):
        for j in range(map_w+1):
            pygame.draw.rect(screen, colors[map[i][j]], pygame.Rect(i * cell_size, j * cell_size, cell_size, cell_size))

    # ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]


    # screen.blit(ball, ballrect)
    pygame.display.flip()