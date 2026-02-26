import pygame
import map
import random
import entity as ent
import texture
import settings


# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Astraya 2.0")
info = pygame.display.Info()
WINDOW_SCALE = info.current_w - 0.1*info.current_w, info.current_h - 0.1*info.current_h
screen = pygame.display.set_mode(WINDOW_SCALE, pygame.RESIZABLE)

clock = pygame.time.Clock()
running = True
dt = 0

scale_map = int(WINDOW_SCALE[0] // (16*settings.SCALE)) - 1, int(WINDOW_SCALE[1] // (16*settings.SCALE)) - 1

resolution_minimap = 4
scale_minimap = int((scale_map[1]*16*settings.SCALE) // resolution_minimap - 10)

grottes_coords = map.coord_grottes
current_world = "overworld"

nbr_poulet = 100

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

all_sprites = pygame.sprite.Group()

player = ent.Player(texture.texture_player, 1500, 1500)
grotte = ent.Grotte(texture.texture_grotte, 1520, 1520)

for i in range(nbr_poulet):
    all_sprites.add(ent.Chicken(texture.texture_chicken, random.randint(1300, 1600), random.randint(1300, 1600)))
    
all_sprites.add(player)
all_sprites.add(grotte)

last_map_change = pygame.time.get_ticks()
def change_map():
    global current_world, last_map_change
    change_cooldown = 2000
    now = pygame.time.get_ticks()
    if now - last_map_change >= change_cooldown:
        if current_world == "overworld":
            current_world = "cave"
        else: current_world = "overworld"
        last_map_change = now

# CHANGEMENT : Utilisation d'IDs numériques au lieu de strings pour correspondre à map.BIOME_IDS
TILE_COLORS = {
    0: (0, 76, 153),      # ocean - ID 0 au lieu de "ocean"
    3: (144, 238, 144),   # jungle - ID 3 au lieu de "jungle"
    4: (0, 100, 0),       # forest - ID 4 au lieu de "forest"
    5: (128, 128, 128),   # mountains - ID 5 au lieu de "mountains"
    6: (255, 255, 255),   # snow_peak - ID 6 au lieu de "snow_peak"
    7: (255, 0, 0),       # collide - ID 7 au lieu de "collide"
    10: (50, 50, 50),     # rock - ID 10 au lieu de "rock"
    11: (180, 220, 255),  # cave_ice - ID 11 au lieu de "cave_ice"
    12: (150, 0, 150),    # cave_mushroom - ID 12 au lieu de "cave_mushroom"
    13: (120, 120, 120),  # cave_normal - ID 13 au lieu de "cave_normal"
    14: (0, 200, 255),    # cave_crystal - ID 14 au lieu de "cave_crystal"
    15: (255, 80, 0),     # cave_lava - ID 15 au lieu de "cave_lava"
}

# CHANGEMENT : IDs numériques pour les textures
TILE_TEXTURE = {
    2: texture.texture_herbe_upscaled,  # plains - ID 2 au lieu de "plains"
    1: texture.texture_sand_upscaled    # beach - ID 1 au lieu de "beach"
}

map_decouverte = set()

last_update_minimap = 0
minimap_surface = pygame.Surface((scale_minimap * resolution_minimap, scale_minimap * resolution_minimap))

def draw_minimap(x, y, scale, player_position, map_to_show):
    global last_update_minimap
    update_minimap_cooldown = 1000
    now = pygame.time.get_ticks()
    distance_de_vue = 250
    
    posx, posy = player_position
    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)

    if now-last_update_minimap >= update_minimap_cooldown:
        last_update_minimap = now
        minimap_surface.fill((0, 0, 255)) 
        
        for i in range(scale):
            for j in range(scale):
                map_i = tile_cx - scale//2 + i
                map_j = tile_cy - scale//2 + j
                
                # CHANGEMENT : map.SIZE au lieu de len(map_to_show)
                if 0 <= map_j < map.SIZE and 0 <= map_i < map.SIZE:  # Utilise map.SIZE (constante) au lieu de len()
                    if (map_i, map_j) in map_decouverte:
                        # CHANGEMENT : Accès NumPy [y, x] au lieu de [y][x]
                        biome_id = map_to_show[map_j, map_i]  # NumPy array : virgule au lieu de double crochet
                        color = TILE_COLORS.get(biome_id, (0, 0, 255))  # Récupère la couleur selon l'ID
                    else:
                        color = (189, 189, 189)
                    pygame.draw.rect(minimap_surface, color, (i * resolution_minimap, j * resolution_minimap, resolution_minimap, resolution_minimap))

        for sprite in all_sprites:
            if sprite.show_on_minimap:
                if abs(player.x - sprite.x) < distance_de_vue and abs(player.y - sprite.y) < distance_de_vue:
                    ptile_x = int(sprite.x // 16)
                    ptile_y = int(sprite.y // 16)
                    
                    rel_x = ptile_x - tile_cx + scale // 2
                    rel_y = ptile_y - tile_cy + scale // 2
                    
                    px = int(rel_x * resolution_minimap)
                    py = int(rel_y * resolution_minimap)
                    if (ptile_x, ptile_y) in map_decouverte:
                        if x <= px < x + scale * resolution_minimap and y <= py < y + scale * resolution_minimap:
                            sprite.draw_minimap(resolution_minimap, minimap_surface, scale, tile_cx, tile_cy)

    pygame.draw.rect(screen, "orange", (x- resolution_minimap,  y- resolution_minimap, 
                        scale * resolution_minimap + resolution_minimap*2, 
                        scale * resolution_minimap + resolution_minimap*2))

    screen.blit(minimap_surface, (x, y))


map_cache = pygame.Surface ((scale_map[0] * 16* settings.SCALE, scale_map[1]  * 16 * settings.SCALE))

def draw_map(x, y, scalex, scaley, player_position, map_to_show):
    global TILE_COLORS
    posx, posy = player_position  

    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)

    offset_x = (posx % 16) * settings.SCALE
    offset_y = (posy % 16) * settings.SCALE

    map_cache.fill("blue")
    for i in range(scalex + 1):
        for j in range(scaley + 1):
            map_i = tile_cx - scalex//2 + i
            map_j = tile_cy - scaley//2 + j

            draw_x = i * 16 * settings.SCALE
            draw_y = j * 16 * settings.SCALE

            if (tile_cx - map_i)**2 + (tile_cy - map_j)**2 < 20**2:
                map_decouverte.add((map_i, map_j))
            
            # CHANGEMENT : map.SIZE au lieu de len(map_to_show)
            if map_i < 0 or map_j < 0 or map_j >= map.SIZE or map_i >= map.SIZE:  # Utilise map.SIZE
                pygame.draw.rect(map_cache, "blue", (draw_x, draw_y, 16*settings.SCALE, 16*settings.SCALE))
            else:
                # CHANGEMENT : Accès NumPy [y, x] et récupération de l'ID biome + variant
                biome_id = map_to_show[map_j, map_i]  # NumPy : virgule au lieu de double crochet
                
                # CHANGEMENT : Vérification de l'ID au lieu de string.startswith()
                if biome_id in TILE_TEXTURE:  # Vérifie l'ID numérique (1 ou 2)
                    # CHANGEMENT : Récupération du variant depuis map.texture_variants
                    variant = map.texture_variants[map_j, map_i] % len(TILE_TEXTURE[biome_id])  # Utilise l'array de variants
                    map_cache.blit(TILE_TEXTURE[biome_id][variant], (draw_x, draw_y))
                elif biome_id in TILE_COLORS:  # Vérifie l'ID numérique
                    pygame.draw.rect(map_cache, TILE_COLORS[biome_id], (draw_x, draw_y, 16*settings.SCALE, 16*settings.SCALE))
                else:
                    pygame.draw.rect(map_cache, "blue", (draw_x, draw_y, 16*settings.SCALE, 16*settings.SCALE))

    for sprite in all_sprites:
        if sprite is not player:
            sprite.draw(scalex, scaley, map_cache, settings.SCALE, posx, posy)
        
    screen.blit(map_cache, (x - offset_x, y - offset_y))

    # bords sur screen
    pygame.draw.rect(screen, "white", (x-16*settings.SCALE, y-16*settings.SCALE, scalex*16*settings.SCALE + 32*settings.SCALE, 16*settings.SCALE))
    pygame.draw.rect(screen, "white", (x-16*settings.SCALE, y+scaley*16*settings.SCALE -16*settings.SCALE, scalex*16*settings.SCALE + 32*settings.SCALE, 32*settings.SCALE))
    pygame.draw.rect(screen, "white", (x-16*settings.SCALE, y-16*settings.SCALE, 16*settings.SCALE, scalex*16*settings.SCALE))
    pygame.draw.rect(screen, "white", (x+scalex*16*settings.SCALE -16*settings.SCALE, y-16*settings.SCALE, 32*settings.SCALE, scalex*16*settings.SCALE))

    screen.blit(player.sprite[player.texture_index], (x + scalex//2 * 16 * settings.SCALE, y + scaley//2 * 16 * settings.SCALE))

def drawcoeurs(x, y, nbcoeurs):
    for i in range(nbcoeurs):
        screen.blit(texture.texture_coeur_upscaled, (x + (i*(texture.texture_coeur_upscaled.get_width()+8)), y))

font_to_write = pygame.font.SysFont(None, 24)

def draw_coordinates(x, y, pos):
    text = font_to_write.render(f"Coordinates: (x: {int(pos[0])//16}, y: {int(pos[1])//16})", True, "red")
    screen.blit(text, (x, y))

def draw_fps(x, y):
    fps = clock.get_fps()
    text = font_to_write.render(f"FPS: ({fps:.2f})", True, "red")
    screen.blit(text, (x, y))
        
chunk_grid = Chunk(chunk_size=64)

# CHANGEMENT : SUPPRESSION DU tile_index_cache car remplacé par map.texture_variants
# Plus besoin de parcourir toute la map pour extraire les variants, ils sont déjà dans un array NumPy

# ANCIEN CODE AVANT CHANGEMENT :
# tile_index_cache = {}
# for j, row in enumerate(map.map):
#     for i, tile in enumerate(row):
#         if "*" in tile:
#             tile_index_cache[(i, j)] = int(tile.split("*")[1])

# RAISON : map.texture_variants contient déjà tous les variants (0-15) pour chaque tile

# boucle de jeu
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for sprite in all_sprites:
        if sprite is not player:
            dist = abs(player.x - sprite.x) + abs(player.y - sprite.y)
            if dist < settings.RENDER_DISTANCE:
                sprite.update(dt, chunk_grid, player.x, player.y) 
    
    chunk_grid.clear()
    chunk_grid.insert(player)
    for sprite in all_sprites:
        chunk_grid.insert(sprite)
    
    player.update()
        
    keys = pygame.key.get_pressed()
    player.input(keys, dt, chunk_grid)

    for sprite in all_sprites:
        if isinstance(sprite, ent.Object):
            if sprite.collides_with(player.collide_box):
                change_map()

    scalemapx, scalemapy = scale_map
    
    # CHANGEMENT : Utilisation de map.cave au lieu de map.cave_biomes
    if current_world == "overworld":
        draw_map(4*settings.SCALE, 4*settings.SCALE, scalemapx, scalemapy, player.get_pos(), map.map)
    else:
        draw_map(4*settings.SCALE, 4*settings.SCALE, scalemapx, scalemapy, player.get_pos(), map.cave)  # map.cave au lieu de map.cave_biomes

    drawcoeurs(10, scalemapy*16*settings.SCALE + 16, 10)
    draw_coordinates(8*settings.SCALE, 8*settings.SCALE, player.get_pos())
    draw_fps(8*settings.SCALE, 16*settings.SCALE)

    if keys[pygame.K_TAB]:
        draw_minimap(WINDOW_SCALE[0] // 2 - (scale_minimap*resolution_minimap)//2, (4*settings.SCALE)+ (scalemapy*16*settings.SCALE) // 2 - (scale_minimap*resolution_minimap)//2, scale_minimap, player.get_pos(), map.map)
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()