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

nbr_poulet = 10

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

def create_texture_basic(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(textures, posx + (i * 16), posy, 16, 16))
    
    tab_upscaled = []
    for i in range(len(tab)):
        tab_upscaled.append(pygame.transform.scale(tab[i], (tab[i].get_width() * SCALE, tab[i].get_height()*SCALE)))
        
    return tab_upscaled

def create_texture_with_rotation(posx, posy, nbr):
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

texture_herbe_upscaled = create_texture_with_rotation(0, 0, 3)
texture_sand_upscaled = create_texture_with_rotation(0, 16, 3)

texture_chicken = create_texture_basic(0, 48, 12)




#class du poulet
class Chicken:
    def __init__(self, x=10, y=10):
        self.x = float(x * 16)
        self.y = float(y * 16)
        self.direction = random.randint(1, 4)
        self.last_move_time = 0
        self.texture_index = 0
        self.last_animation = 0
        self.emoting_state = True
        self.emoting_start = 0
        self.last_emoting = 0
        self.move_count = 0
        self.last_direction = 0
        self.speed = 200

    def update(self):
        self.emoting()
        now = pygame.time.get_ticks()
        if self.emoting_state:
            if now - self.last_emoting >= random.randint(5000, 8000):
                self.emoting_state = False
                self.move_count = 0
        else:
            if now - self.last_move_time >= random.randint(500, 3000):
                attempts = 0
                while self.direction == self.last_direction or self.direction == self.direction_opposee(self.last_direction):
                    self.direction = random.randint(1, 4)
                    attempts += 1
                    if attempts >= 10:
                        self.direction = self.last_direction
                        break
                self.last_direction = self.direction
                
                if self.direction == 1:
                    self.move(self.speed*dt, 0, random.randint(0, 2))
                elif self.direction == 2:
                    self.move(-self.speed*dt, 0, random.randint(5, 7))
                elif self.direction == 3:
                    self.move(0, -self.speed*dt, random.randint(10, 11))
                elif self.direction == 4: 
                    self.move(0, -self.speed*dt, random.randint(8, 9))

                self.last_move_time = now
                
                if self.move_count >= random.randint(5, 20):
                    self.emoting_state = True
                    self.emoting_start = now
                    self.last_emoting = now
                    
    def move(self, dx, dy, texture):
        new_x = self.x + dx
        new_y = self.y + dy
        tile_x = int(new_x // 16)
        tile_y = int(new_y // 16)
        self.texture_index = texture
        self.x = new_x
        self.y = new_y
        
                
    def emoting(self):
        now = pygame.time.get_ticks()
        if self.emoting_state:
            if now - self.last_animation >= random.randint(1000, 3000):
                if self.texture_index == 0:
                    self.texture_index = 3
                else: 
                    self.texture_index = 0 
                self.last_animation = now
                
    def direction_opposee(self, direction):
        if direction == 1: return 2 
        if direction == 2: return 1
        if direction == 3: return 4 
        if direction == 4: return 3

#class du joueur
class Player:
    def __init__(self, x=0, y=0):
        self.x = float(x * 16)  # position en pixels monde
        self.y = float(y * 16)
        self.speed = 100  # pixels par seconde
    
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        tile_x = int(new_x // 16)
        tile_y = int(new_y // 16)
        
        if veriftile(tile_x, tile_y):
            self.x = new_x
            self.y = new_y

    def input(self, keys, dt):
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.move(0, -self.speed * dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(0, self.speed * dt)
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.move(-self.speed * dt, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(self.speed * dt, 0)

    def get_pos(self):
        return (self.x, self.y)  # en pixels
    
    
tab_poulet = []
for i in range(nbr_poulet):
    tab_poulet.append(Chicken())

#joueur    
player = Player()

    
#afficher la minimap (appeler dans draw_map())    
def draw_minimap(x, y, scale, player_position):
    pygame.draw.rect(screen, "orange", (x-resolution_minimap, y-resolution_minimap, scale*resolution_minimap+resolution_minimap*2, scale*resolution_minimap+resolution_minimap*2))
    posx, posy = player_position
    
    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)
    
    for i in range(scale):
        for j in range(scale):
            map_i = tile_cx - scale//2 + i
            map_j = tile_cy - scale//2 + j
            

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
    posx, posy = player_position  # maintenant en pixels monde

    # Tile centrale
    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)

    # Décalage sub-tile (pour le smooth scrolling)
    offset_x = int(posx % 16) * SCALE
    offset_y = int(posy % 16) * SCALE

    for i in range(scalex + 1):  # +1 pour couvrir le décalage
        for j in range(scaley + 1):
            map_i = tile_cx - scalex//2 + i
            map_j = tile_cy - scaley//2 + j

            # Position à l'écran avec le décalage appliqué
            draw_x = x + (i * 16 * SCALE) - offset_x
            draw_y = y + (j * 16 * SCALE) - offset_y

            if map_i < 0 or map_j < 0 or map_j >= len(map.map) or map_i >= len(map.map[map_j]):
                pygame.draw.rect(screen, "blue", (draw_x, draw_y, 16*SCALE, 16*SCALE))
            else:
                if map.map[map_j][map_i] == "ocean":
                    pygame.draw.rect(screen, "blue", (draw_x, draw_y, 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i].startswith("beach"):
                    index = int(map.map[map_j][map_i].split("_")[1])
                    screen.blit(texture_sand_upscaled[index - 1], (draw_x, draw_y))
                elif map.map[map_j][map_i] == "jungle":
                    pygame.draw.rect(screen, "lightgreen", (draw_x, draw_y, 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i].startswith("plains"):
                    index = int(map.map[map_j][map_i].split("_")[1])
                    screen.blit(texture_herbe_upscaled[index - 1], (draw_x, draw_y))
                elif map.map[map_j][map_i] == "mountains":
                    pygame.draw.rect(screen, "gray", (draw_x, draw_y, 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == "snow_peak":
                    pygame.draw.rect(screen, "white", (draw_x, draw_y, 16*SCALE, 16*SCALE))
                elif map.map[map_j][map_i] == "forest":
                    pygame.draw.rect(screen, "darkgreen", (draw_x, draw_y, 16*SCALE, 16*SCALE))

                for poulet in tab_poulet:
                    px = x + (poulet.x - (tile_cx - scalex//2) * 16) * SCALE - offset_x
                    py = y + (poulet.y - (tile_cy - scaley//2) * 16) * SCALE - offset_y

                    if 0 <= px < scalex*16*SCALE and 0 <= py < scaley*16*SCALE:
                        screen.blit(texture_chicken[poulet.texture_index], (px, py))

    # Le joueur reste toujours au centre de l'écran
    pygame.draw.rect(screen, "orange", (x + (scalex//2 * 16 * SCALE), y + (scaley//2 * 16 * SCALE), 16*SCALE, 16*SCALE))

    draw_minimap(x + scalex*16*SCALE - resolution_minimap*scale_minimap - resolution_minimap, y + resolution_minimap, scale_minimap, player_position)
    
    

texture_coeur = get_sprite(textures, 0, 241, 16, 16)
texture_coeur_upscaled = pygame.transform.scale(texture_coeur, (texture_coeur.get_width()*SCALE, texture_coeur.get_height()*SCALE))    
#afficher les coeurs
def drawcoeurs(x, y, nbcoeurs):
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
    text = font_to_write.render(f"Coordinates: ({pos[0]:.2f}, {pos[1]:.2f})", True, "red")
    screen.blit(text, (x, y))
    
def draw_fps(x, y):
    font_to_write = pygame.font.SysFont(None, 24)
    fps = clock.get_fps()
    text = font_to_write.render(f"FPS: ({fps:.2f})", True, "red")
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
    
    draw_fps(8*SCALE, 16*SCALE)
    
    for i in range(len(tab_poulet)):
        tab_poulet[i].update()
    
    keys = pygame.key.get_pressed()
    player.input(keys, dt)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()


    