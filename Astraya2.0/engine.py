import pygame
import map
import random
import os
import entity as ent



SCALE = 2

# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Astraya 2.0")
info = pygame.display.Info()
WINDOW_SCALE = info.current_w - 0.1*info.current_w, info.current_h - 0.1*info.current_h
screen = pygame.display.set_mode(WINDOW_SCALE, pygame.RESIZABLE)
#screen = pygame.display.set_mode((GAME_W * SCALE, GAME_H * SCALE), pygame.RESIZABLE)

#Chargement des textures
textures = pygame.image.load(os.path.join('Astraya2.0' ,'assets', 'textures', 'astrayatextures.png'))

clock = pygame.time.Clock()
running = True
dt = 0

scale_map = int(WINDOW_SCALE[0] // (16*SCALE)) - 1, int(WINDOW_SCALE[1] // (16*SCALE)) - 1

resolution_minimap = 4
scale_minimap = int((scale_map[1]*16*SCALE) // resolution_minimap - 10)

grottes_coords = map.coord_grottes

<<<<<<< HEAD

nbr_poulet = 1000
=======
nbr_poulet = 10000
>>>>>>> 43250310f09990482f14834a93307d0deaf374d8



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

texture_herbe_upscaled = create_texture_with_rotation(0, 0, 4)
texture_sand_upscaled = create_texture_with_rotation(0, 16, 4)

texture_chicken = create_texture_basic(0, 48, 12)




class Chunk:
    def __init__(self, chunk_size=32):
        self.chunk_size = chunk_size
        self.grid = {}
        
    def get_chunk(self, x ,y):
        return (int(x // self.chunk_size), int(y // self.chunk_size))
    
    def clear(self):
        self.grid.clear()
    
    def insert(self, entity):
        chunk = self.get_chunk(entity.x, entity.y)
        if chunk not in self.grid:
            self.grid[chunk] = []
        self.grid[chunk].append(entity)
        
    def get_nearby(self, x, y):
        cx, cy = self.get_chunk(x, y)
        nearby = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                chunk = (cx +dx, cy+dy)
                if chunk in self.grid:
                    nearby.extend(self.grid[chunk])
        return nearby

    
    
tab_poulet = []
for i in range(nbr_poulet):
    tab_poulet.append(ent.Chicken(random.randint(0, 3000), random.randint(0,3000)))

#joueur    
player = ent.Player()

minimap_surface = pygame.Surface((scale_minimap * resolution_minimap, scale_minimap * resolution_minimap))
last_minimap_tile = (None, None)
    
    
TILE_COLORS = {"ocean": (0, 0, 255), "jungle": (144, 238, 144),"mountains": (128, 128, 128),"snow_peak": (255, 255, 255),"forest": (0, 100, 0), "collide" : (255, 0 ,0), "beach" : (237, 201, 88), "plains" : (34, 139, 34)}
TILE_TEXTURE = {"plains" : texture_herbe_upscaled, "beach" : texture_sand_upscaled}
#afficher la minimap (appeler dans draw_map())    

map_decouverte = set()

texture_poulet_minimap = []
for i in range(len(texture_chicken)):
    texture_poulet_minimap.append(pygame.transform.scale(texture_chicken[i], (texture_chicken[i].get_width() * 0.5, texture_chicken[i].get_height() * 0.5)))

def draw_minimap(x, y, scale, player_position, map_to_show):
    global last_minimap_tile
    
    distance_de_vue = 250
    
    posx, posy = player_position
    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)
    

    if (tile_cx, tile_cy) != last_minimap_tile:
        last_minimap_tile = (tile_cx, tile_cy)
        minimap_surface.fill((0, 0, 255)) 
        
        for i in range(scale):
            for j in range(scale):
                map_i = tile_cx - scale//2 + i
                map_j = tile_cy - scale//2 + j
                

                if 0 <= map_j < len(map_to_show) and 0 <= map_i < len(map_to_show[map_j]):
                    if (map_i, map_j) in map_decouverte:
                        tile = map_to_show[map_j][map_i]
                        tile_base = tile.split("*")[0]
                        color = TILE_COLORS[tile_base]
                    else:
                        color = (189, 189, 189)
                    pygame.draw.rect(minimap_surface, color, (i * resolution_minimap, j * resolution_minimap, resolution_minimap, resolution_minimap))

    # bord orange
    pygame.draw.rect(screen, "orange", (x - resolution_minimap, y - resolution_minimap, 
                     scale * resolution_minimap + resolution_minimap*2, 
                     scale * resolution_minimap + resolution_minimap*2))

    screen.blit(minimap_surface, (x, y))
    
    for poulet in tab_poulet:
        if abs(player.x - poulet.x) < distance_de_vue and abs(player.y - poulet.y) < distance_de_vue:
            # position du poulet en tiles
            ptile_x = int(poulet.x // 16)
            ptile_y = int(poulet.y // 16)
            
            rel_x = ptile_x - tile_cx + scale // 2
            rel_y = ptile_y - tile_cy + scale // 2
            
            px = x + int(rel_x * resolution_minimap)
            py = y + int(rel_y * resolution_minimap)
            
            if (ptile_x, ptile_y) in map_decouverte:
                if x <= px < x + scale * resolution_minimap and y <= py < y + scale * resolution_minimap:
                    texture = texture_poulet_minimap[poulet.texture_index]
                    screen.blit(texture, (px-8, py-8))

    pygame.draw.rect(screen, "orange", (x + (scale//2 * resolution_minimap), y + (scale//2 * resolution_minimap), 4, 4))


map_cache = pygame.Surface ((scale_map[0] * 16* SCALE, scale_map[1]  * 16 * SCALE))
last_map_tile = (None, None)

#afficher le viewport principal
def draw_map(x, y, scalex, scaley, player_position, map_to_show):
    global last_map_tile, TILE_COLORS
    posx, posy = player_position  

    # tile centrale
    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)

    offset_x = int(posx % 16) * SCALE
    offset_y = int(posy % 16) * SCALE

    if (tile_cx, tile_cy) != last_map_tile:
        last_map_tile = (tile_cx, tile_cy)
        map_cache.fill("blue")
        for i in range(scalex + 1):
            for j in range(scaley + 1):
                map_i = tile_cx - scalex//2 + i
                map_j = tile_cy - scaley//2 + j

                draw_x = i * 16 * SCALE
                draw_y = j * 16 * SCALE

                if (tile_cx - map_i)**2 + (tile_cy - map_j)**2 < 20**2:
                    map_decouverte.add((map_i, map_j))
                    

                if map_i < 0 or map_j < 0 or map_j >= len(map_to_show) or map_i >= len(map_to_show[map_j]):
                    pygame.draw.rect(map_cache, "blue", (draw_x, draw_y, 16*SCALE, 16*SCALE))
                else:
                    tile = map_to_show[map_j][map_i]
                    tile_base = tile.split("*")[0]
                    if tile_base in TILE_TEXTURE:
                        index = tile_index_cache.get((map_i, map_j), 0)
                        map_cache.blit(TILE_TEXTURE[tile_base][index], (draw_x, draw_y))
                    elif tile in TILE_COLORS:
                        pygame.draw.rect(map_cache, TILE_COLORS[tile], (draw_x, draw_y, 16*SCALE, 16*SCALE))
                    else:
                        pygame.draw.rect(map_cache, "blue", (draw_x, draw_y, 16*SCALE, 16*SCALE))

<<<<<<< HEAD
    
    screen.blit(map_cache, (x - offset_x, y - offset_y))
    
    #poulets         
=======
    # ===== 2. DESSINER LES GROTTES =====
    for grotte_x, grotte_y in grottes_coords:
        # Position de la grotte par rapport à la caméra
        gx = x + (grotte_x * 16 - (tile_cx - scalex//2) * 16) * SCALE - offset_x
        gy = y + (grotte_y * 16 - (tile_cy - scaley//2) * 16) * SCALE - offset_y

        # Ne dessiner que si visible à l'écran
        if -16*SCALE <= gx < (scalex+1)*16*SCALE and -16*SCALE <= gy < (scaley+1)*16*SCALE:
            
            # Rectangle temporaire (jaune pour les voir facilement)
            pygame.draw.rect(screen, "pink", (int(gx), int(gy), 16*SCALE, 16*SCALE))
            pygame.draw.circle(screen, "black", (int(gx + 8*SCALE), int(gy + 8*SCALE)), 4*SCALE)


>>>>>>> 43250310f09990482f14834a93307d0deaf374d8
    for poulet in tab_poulet:
        px = x + (poulet.x - (tile_cx - scalex//2) * 16) * SCALE - offset_x
        py = y + (poulet.y - (tile_cy - scaley//2) * 16) * SCALE - offset_y

        if 0 <= px < scalex*16*SCALE and 0 <= py < scaley*16*SCALE:
            screen.blit(texture_chicken[poulet.texture_index], (px, py))

    # bords sur screen, avec coordonnées écran
    pygame.draw.rect(screen, "white", (x-16*SCALE, y-16*SCALE, scalex*16*SCALE + 32*SCALE, 16*SCALE))
    pygame.draw.rect(screen, "white", (x-16*SCALE, y+scaley*16*SCALE -16*SCALE, scalex*16*SCALE + 32*SCALE, 32*SCALE))
    pygame.draw.rect(screen, "white", (x-16*SCALE, y-16*SCALE, 16*SCALE, scalex*16*SCALE))
    pygame.draw.rect(screen, "white", (x+scalex*16*SCALE -16*SCALE, y-16*SCALE, 32*SCALE, scalex*16*SCALE))
    #player
    pygame.draw.rect(screen, "orange", (x + (scalex//2 * 16 * SCALE), y + (scaley//2 * 16 * SCALE), 16*SCALE, 16*SCALE))
    

texture_coeur = get_sprite(textures, 0, 241, 16, 16)
texture_coeur_upscaled = pygame.transform.scale(texture_coeur, (texture_coeur.get_width()*SCALE, texture_coeur.get_height()*SCALE))    
#afficher les coeurs
def drawcoeurs(x, y, nbcoeurs):
    for i in range(nbcoeurs):
        screen.blit(texture_coeur_upscaled, (x + (i*(texture_coeur_upscaled.get_width()+8)), y))
                    

font_to_write = pygame.font.SysFont(None, 24)
#afficher les coordonés (peut etre temp)
def draw_coordinates(x, y, pos):
    text = font_to_write.render(f"Coordinates: (x: {int(pos[0])//16}, y: {int(pos[1])//16})", True, "red")
    screen.blit(text, (x, y))

#afficher fps   
def draw_fps(x, y):
    fps = clock.get_fps()
    text = font_to_write.render(f"FPS: ({fps:.2f})", True, "red")
    screen.blit(text, (x, y))
        
chunk_grid = Chunk(chunk_size=64)

tile_index_cache = {}
for j, row in enumerate(map.map):
    for i, tile in enumerate(row):
        if "*" in tile:
            tile_index_cache[(i, j)] = int(tile.split("*")[1])

RENDER_DISTANCE = 1000
#boucle de jeu
while running:
    #quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    scalemapx, scalemapy = scale_map
    
    draw_map(4*SCALE, 4*SCALE, scalemapx, scalemapy, player.get_pos(), map.map)
    
    
    drawcoeurs(10, scalemapy*16*SCALE + 16, 10)
    
    draw_coordinates(8*SCALE, 8*SCALE, player.get_pos())
    
    draw_fps(8*SCALE, 16*SCALE)

    for poulet in tab_poulet:
        dist = abs(player.x - poulet.x) + abs(player.y - poulet.y)  # manhattan, plus rapide que sqrt
        if dist < RENDER_DISTANCE:
            poulet.update(dt, chunk_grid)
    
    chunk_grid.clear()
    chunk_grid.insert(player)
    for p in tab_poulet:
        chunk_grid.insert(p)
    
    player.update()
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB]:
        draw_minimap(WINDOW_SCALE[0] // 2 - (scale_minimap*resolution_minimap)//2, (4*SCALE)+ (scalemapy*16*SCALE) // 2 - (scale_minimap*resolution_minimap)//2, scale_minimap, player.get_pos(), map.map)
    player.input(keys, dt, chunk_grid)

    
    
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

