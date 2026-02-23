# Example file showing a circle moving on screen
import pygame
import map

GAME_W = 640 
GAME_H = 480
SCALE = 2

# pygame setup
pygame.init()
screen = pygame.display.set_mode((GAME_W * SCALE, GAME_H * SCALE))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = 3, 3

scale_map = 39, 19

timing_step = 10 #frame a attendre entre chaque déplacement du joueur 60 frames = 1 seconde

timing_step_count = timing_step


def draw_player():
    pygame.draw.rect(screen, "yellow", (screen.get_width()//2-8*SCALE, screen.get_height()//2-8*SCALE, 16*SCALE, 16*SCALE))
    
def draw_minimap(x, y, scale, player_position):
    pygame.draw.rect(screen, "orange", (x-8, y-8, scale*8+16, scale*8+16))
    posx, posy = player_position
    for i in range(scale):
        for j in range(scale):
            map_i = posx - scale//2 + i
            map_j = posy - scale//2 + j
            if map_i < 0 or map_j < 0 or map_j >= len(map.map) or map_i >= len(map.map[map_j]):
                pygame.draw.rect(screen, "blue", (x + (i*8), y + (j*8), 8, 8))
            else:
                if map.map[map_j][map_i] == 0:
                    pygame.draw.rect(screen, "black", (x + (i*8), y + (j*8), 8, 8))
                elif map.map[map_j][map_i] == 1:
                    pygame.draw.rect(screen, "grey", (x + (i*8), y + (j*8), 8, 8))
                elif map.map[map_j][map_i] == 3:
                    pygame.draw.rect(screen, "red", (x + (i*8), y + (j*8), 8, 8))
    
    #player
    pygame.draw.rect(screen, "yellow", (x + (scale//2*8), y + (scale//2*8), 8, 8))

    
def draw_map(x, y, scalex, scaley, player_position):
    posx, posy = player_position
    for i in range(scalex):
        for j in range(scaley):
            map_i = posx - scalex//2 + i
            map_j = posy - scaley//2 + j
            if map_i < 0 or map_j < 0 or map_j >= len(map.map) or map_i >= len(map.map[map_j]):
                pygame.draw.rect(screen, "blue", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
            else:
                if map.map[map_j][map_i] == 0:
                    pygame.draw.rect(screen, "black", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == 1:
                    pygame.draw.rect(screen, "grey", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == 3:
                    pygame.draw.rect(screen, "red", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
    
    #player
    pygame.draw.rect(screen, "yellow", (x + (scalex//2*16*SCALE), y + (scaley//2*16*SCALE), 16*SCALE, 16*SCALE))
    
    scale_minimap = 25
    
    draw_minimap(x+scalex*16*SCALE - 8*scale_minimap - 8, y+8, scale_minimap, player_pos)
    
def drawcoeurs(x, y, nbcoeurs):
    for i in range(nbcoeurs):
        pygame.draw.rect(screen, "red", (x + (i*16+16), y, 16, 16))
                    
                    
def veriftile(x, y):
    if x < 0 or y < 0 or y >= len(map.map) or x >= len(map.map[y]) or x == None or y == None:
        return False
    elif map.map[y][x] in map.collide_tiles:
        return False
    else:
        return True

while running:
    
    player_pos_x, player_pos_y = player_pos
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    scalemapx, scalemapy = scale_map
    
    draw_map(4*SCALE, 4*SCALE, scalemapx, scalemapy, player_pos)
    
    drawcoeurs(10, scalemapy*16*SCALE + 16, 10)
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] or keys[pygame.K_UP]:
        if veriftile(player_pos_x, player_pos_y-1):
            if timing_step_count == 0:
                timing_step_count = timing_step
                player_pos_y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if veriftile(player_pos_x, player_pos_y+1):
            if timing_step_count == 0:
                timing_step_count = timing_step
                player_pos_y += 1
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        if veriftile(player_pos_x-1, player_pos_y):
            if timing_step_count == 0:
                timing_step_count = timing_step
                player_pos_x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if veriftile(player_pos_x+1, player_pos_y):
            if timing_step_count == 0:
                timing_step_count = timing_step
                player_pos_x += 1

    player_pos = (player_pos_x, player_pos_y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    if timing_step_count > 0:
        timing_step_count -= 1
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()


    