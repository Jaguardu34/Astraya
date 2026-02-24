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

scale_map = 39, 19

resolution_minimap = 4
scale_minimap = 65

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

def create_texture(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(textures, posx + (i * 16), posy, 16, 16))
        tab.append(pygame.transform.rotate(get_sprite(textures, posx + (i * 16), posy, 16, 16), 90))
        tab.append(pygame.transform.rotate(get_sprite(textures, posx + (i * 16), posy, 16, 16), -90))
        tab.append(pygame.transform.rotate(get_sprite(textures, posx + (i * 16), posy, 16, 16), 180))
    
    tab_upscaled = []
    for i in range(len(tab)):
        tab_upscaled.append(pygame.transform.scale(tab[i], (tab[i].get_width() * SCALE, tab[i].get_height()*SCALE)))
        
    return tab_upscaled

texture_herbe_upscaled = create_texture(0, 0, 3)
texture_sand_upscaled = create_texture(0, 16, 3)

    
texture_chicken = get_sprite(textures, 0, 48, 16, 16)
texture_chicken_upscaled = pygame.transform.scale(texture_chicken, (texture_chicken.get_width() * SCALE, texture_chicken.get_height()*SCALE))


#class du poulet
class Chicken:
    def __init__(self, x=10, y=10):
        self.x = x
        self.y = y
        self.direction = random.randint(1, 4)
        self.last_move_time = 0
        self.move_cooldown = 1000

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= self.move_cooldown:
            self.direction = random.randint(1,4)
            if self.direction == 1:
                if veriftile(self.x + 1, self.y):
                    self.x += 1
            elif self.direction == 2:
                if veriftile(self.x -1 , self.y):
                    self.x -= 1
            elif self.direction == 3:
                if veriftile(self.x, self.y + 1):
                    self.y += 1
            else: 
                if veriftile(self.x, self.y - 1):
                    self.y - 1
            self.last_move_time = now
    


#class du joueur
class Player:
    def __init__(self, x=0, y=0, nb_coeurs=10):
        self.x = x
        self.y = y
        self.nb_coeurs = nb_coeurs
        self.last_move = 0
        self.move_cooldown = 200 #millisecondes entre chaque mvt

    def move(self, dx, dy):
        now = pygame.time.get_ticks()
        if now - self.last_move >= self.move_cooldown:
            if veriftile(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy
            self.last_move = now


    def input(self, keys):
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(0, 1)
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(1, 0)

    def get_pos(self):
        return (self.x, self.y)
    
#creation d'un poulet de test et du joueur
player = Player()

poulet = Chicken()

    
#afficher la minimap (appeler dans draw_map())    
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
                elif map.map[map_j][map_i].startswith("beach"):
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

#afficher le viewport principal
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
                elif map.map[map_j][map_i].startswith("beach"):
                    index = int(map.map[map_j][map_i].split("_")[1])
                    screen.blit(texture_sand_upscaled[index - 1], (x + (i * 16 * SCALE), y + (j * 16 * SCALE)))
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
                   
                   
                if map_j == poulet.x and map_i == poulet.y:
                    screen.blit(texture_chicken_upscaled, (x + (i * 16 * SCALE), y + (j * 16 * SCALE)))
    
    #player
    pygame.draw.rect(screen, "orange", (x + (scalex//2*16*SCALE), y + (scaley//2*16*SCALE), 16*SCALE, 16*SCALE))   
    
    draw_minimap(x+scalex*16*SCALE - resolution_minimap*scale_minimap - resolution_minimap, y+resolution_minimap, scale_minimap, player_position)
    
    
#afficher les coeurs
def drawcoeurs(x, y, nbcoeurs):
    texture_coeur = get_sprite(textures, 0, 241, 16, 16)
    texture_coeur_upscaled = pygame.transform.scale(texture_coeur, (texture_coeur.get_width()*SCALE, texture_coeur.get_height()*SCALE))
    for i in range(nbcoeurs):
        screen.blit(texture_coeur_upscaled, (x + (i*(texture_coeur_upscaled.get_width()+8)), y))
                    
#verif collisions                   
def veriftile(x, y):
    if x < 0 or y < 0 or y >= len(map.map) or x >= len(map.map[y]) or x == None or y == None:
        return False
    elif map.map[y][x] in map.collide_tiles:
        return False
    else:
        return True

#afficher les coordonés (peut etre temp)
def draw_coordinates(x, y, pos):
    font_to_write = pygame.font.SysFont(None, 24)
    text = font_to_write.render(f"Coordinates: ({pos[0]}, {pos[1]})", True, "red")
    screen.blit(text, (x, y))


        

#boucle de jeu
while running:
    #quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    scalemapx, scalemapy = scale_map
    
    draw_map(4*SCALE, 4*SCALE, scalemapx, scalemapy, player.get_pos())
    
    drawcoeurs(10, scalemapy*16*SCALE + 16, 10)
    
    draw_coordinates(8*SCALE, 8*SCALE, player.get_pos())
    
    poulet.update()
    
    keys = pygame.key.get_pressed()
    player.input(keys)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()


    