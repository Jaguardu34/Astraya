import pygame
from generate_map import *
import random
import entity as ent
import texture
from settings import *
import map_render

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

scale_map = int(WINDOW_SCALE[0] // (16*  SCALE)) - 1, int(WINDOW_SCALE[1] // (16*  SCALE)) - 1

resolution_minimap = 4
scale_minimap = int((scale_map[1]*16*  SCALE) // resolution_minimap - 10)

grottes_coords = coord_grottes
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

player = ent.Player(texture.texture_player, map, x=1500, y=1500)
grotte = ent.Grotte(texture.texture_grotte, map, x=1520, y=1520)

for i in range(nbr_poulet):
    all_sprites.add(ent.Chicken(texture.texture_chicken, map, x=random.randint(1300, 1600), y=random.randint(1300, 1600)))
    
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

main_map = map_render.Map(scale_map, screen, all_sprites)
minimap = map_render.Minimap(scale_minimap, resolution_minimap, screen, all_sprites)

while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for sprite in all_sprites:
        if sprite is not player:
            dist = abs(player.x - sprite.x) + abs(player.y - sprite.y)
            if dist <   RENDER_DISTANCE:
                sprite.update(dt, chunk_grid) 
    
    chunk_grid.clear()
    chunk_grid.insert(player)
    for sprite in all_sprites:
        chunk_grid.insert(sprite)
    
    player.update(chunk_grid)
        
    keys = pygame.key.get_pressed()
    player.input(keys, dt)

    for sprite in all_sprites:
        if isinstance(sprite, ent.Object):
            if sprite.collides_with(player.collide_box):
                change_map()

    scalemapx, scalemapy = scale_map
    
    # CHANGEMENT : Utilisation de map.cave au lieu de map.cave_biomes
    if current_world == "overworld":
        main_map.draw(4*  SCALE, 4*  SCALE, player.get_pos(), map, player)
    else:
        main_map.draw(4*  SCALE, 4*  SCALE, player.get_pos(), cave, player)  # map.cave au lieu de map.cave_biomes

    drawcoeurs(10, scalemapy*16*  SCALE + 16, 10)
    draw_coordinates(8*  SCALE, 8*  SCALE, player.get_pos())
    draw_fps(8*  SCALE, 16*  SCALE)

    if keys[pygame.K_TAB]:
        minimap.draw(WINDOW_SCALE[0] // 2 - (scale_minimap*resolution_minimap)//2, (4*  SCALE)+ (scalemapy*16*  SCALE) // 2 - (scale_minimap*resolution_minimap)//2, player.get_pos(), map)

    
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000

pygame.quit()