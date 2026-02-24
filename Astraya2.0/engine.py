# Example file showing a circle moving on screen
import pygame
import map
import random
import os

GAME_W = 640 
GAME_H = 480
SCALE = 2

# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Astraya 2.0")
screen = pygame.display.set_mode((GAME_W * SCALE, GAME_H * SCALE))

#Chargement des textures
textures = pygame.image.load(os.path.join('Astraya2.0' ,'assets', 'textures', 'astrayatextures.png'))

clock = pygame.time.Clock()
running = True
dt = 0

player_pos = random.randint(0, 2000), random.randint(0, 2000)
scale_map = 39, 19

timing_step = 1 #frame a attendre entre chaque déplacement du joueur 60 frames = 1 seconde
timing_step_count = timing_step

resolution_minimap = 4
scale_minimap = 65

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

texture_herbe = []
for i in range(3):
    texture_herbe.append(get_sprite(textures, 0 + (i * 16), 0, 16, 16))
    texture_herbe.append(pygame.transform.rotate(get_sprite(textures, 0 + (i * 16), 0, 16, 16), 90))
    texture_herbe.append(pygame.transform.rotate(get_sprite(textures, 0 + (i * 16), 0, 16, 16), -90))
    texture_herbe.append(pygame.transform.rotate(get_sprite(textures, 0 + (i * 16), 0, 16, 16), 180))

texture_herbe_upscaled = []
for i in range(len(texture_herbe)):
    texture_herbe_upscaled.append(pygame.transform.scale(texture_herbe[i], (texture_herbe[i].get_width() * SCALE, texture_herbe[i].get_height()*SCALE)))


def draw_player():
    pygame.draw.rect(screen, "yellow", (screen.get_width()//2-8*SCALE, screen.get_height()//2-8*SCALE, 16*SCALE, 16*SCALE))
    
    

def draw_minimap(x, y, scale, player_position):
    pygame.draw.rect(screen, "orange", (x-resolution_minimap, y-resolution_minimap, scale*resolution_minimap+resolution_minimap*2, scale*resolution_minimap+resolution_minimap*2))
    posx, posy = player_position
    for i in range(scale):
        for j in range(scale):
            map_i = posx - scale//2 + i
            map_j = posy - scale//2 + j
            if map_i < 0 or map_j < 0 or map_j >= len(map.map) or map_i >= len(map.map[map_j]):
                pygame.draw.rect(screen, "blue", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
            else:
                if map.map[map_j][map_i] == "ocean":
                    pygame.draw.rect(screen, "blue", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                elif map.map[map_j][map_i] == "beach":
                    pygame.draw.rect(screen, "yellow", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                elif map.map[map_j][map_i] == "jungle":
                    pygame.draw.rect(screen, "lightgreen", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                elif map.map[map_j][map_i].startswith("plains"):
                    pygame.draw.rect(screen, "green", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                elif map.map[map_j][map_i] == "mountains":
                    pygame.draw.rect(screen, "gray", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                elif map.map[map_j][map_i] == "snow_peak":
                    pygame.draw.rect(screen, "white", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                elif map.map[map_j][map_i] == "forest":
                    pygame.draw.rect(screen, "darkgreen", (x + (i*resolution_minimap), y + (j*resolution_minimap), resolution_minimap, resolution_minimap))
                
    
    #player
    pygame.draw.rect(screen, "orange", (x + (scale//2*resolution_minimap), y + (scale//2*resolution_minimap), 8, 8))

    
def draw_map(x, y, scalex, scaley, player_position):
    posx, posy = player_position
    for i in range(scalex):
        for j in range(scaley):
            map_i = posx - scalex//2 + i
            map_j = posy - scaley//2 + j
            if map_i < 0 or map_j < 0 or map_j >= len(map.map) or map_i >= len(map.map[map_j]):
                pygame.draw.rect(screen, "blue", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
            else:
                if map.map[map_j][map_i] == "ocean":
                    pygame.draw.rect(screen, "blue", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == "beach":
                    pygame.draw.rect(screen, "yellow", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == "jungle":
                    pygame.draw.rect(screen, "lightgreen", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i].startswith("plains"):
                    index = int(map.map[map_j][map_i].split("_")[1])
                    screen.blit(texture_herbe_upscaled[index - 1], (x + (i * 16 * SCALE), y + (j * 16 * SCALE)))
                elif map.map[map_j][map_i] == "mountains":
                    pygame.draw.rect(screen, "gray", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == "snow_peak":
                    pygame.draw.rect(screen, "white", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == "forest":
                    pygame.draw.rect(screen, "darkgreen", (x + (i*16*SCALE), y + (j*16*SCALE), 16*SCALE, 16*SCALE))
    
    #player
    pygame.draw.rect(screen, "orange", (x + (scalex//2*16*SCALE), y + (scaley//2*16*SCALE), 16*SCALE, 16*SCALE))
    
    
    
    draw_minimap(x+scalex*16*SCALE - resolution_minimap*scale_minimap - resolution_minimap, y+resolution_minimap, scale_minimap, player_position)
    
def drawcoeurs(x, y, nbcoeurs):
    for i in range(nbcoeurs):
        screen.blit(textures, (x + (i*32), y), pygame.Rect(0, 241, 16, 16))
                    
                    
def veriftile(x, y):
    if x < 0 or y < 0 or y >= len(map.map) or x >= len(map.map[y]) or x == None or y == None:
        return False
    elif map.map[y][x] in map.collide_tiles:
        return False
    else:
        return True


def draw_coordinates(x, y, posx, posy):
    font_to_write = pygame.font.SysFont(None, 24)
    text = font_to_write.render(f"Coordinates: ({posx}, {posy})", True, "red")
    screen.blit(text, (x, y))
    


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
    
    draw_coordinates(8*SCALE, 8*SCALE, player_pos_x, player_pos_y)
    

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


    