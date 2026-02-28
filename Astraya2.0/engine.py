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

scale_map = int(WINDOW_SCALE[0] // 32) , int(WINDOW_SCALE[1] // 32) - 1

resolution_minimap = 8
scale_minimap = int((scale_map[1]*32) // resolution_minimap - 10)

grottes_coords = coord_grottes


grottes_coords = coord_grottes  
altitude_map = altitude_map     
cliff_edges = cliff_edges       
nbr_poulet = 100

game_map = map

current_map = game_map

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

entity = pygame.sprite.Group()

player = ent.Player(texture.texture_player, game_map, altitude_map, x=1500, y=1500)
grotte = ent.Grotte(texture.texture_grotte, game_map, altitude_map, x=1520, y=1520)

for i in range(nbr_poulet):
    entity.add(ent.Chicken(texture.texture_chicken, game_map, altitude_map, x=random.randint(1300, 1600), y=random.randint(1300, 1600)))
    
entity.add(player)
entity.add(grotte)

last_map_change = pygame.time.get_ticks()
def change_map():
    global current_map, last_map_change
    change_cooldown = 2000
    now = pygame.time.get_ticks()
    if now - last_map_change >= change_cooldown:
        if current_map is game_map:
            current_map = cave
        else: current_map = game_map
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

main_map = map_render.Map(scale_map, screen, [entity])
minimap = map_render.Minimap(WINDOW_SCALE[1]- 200, 1000, screen, [entity])
minimap_left_corner = map_render.Minimap(240, 200, screen, [entity])

while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    
    
    chunk_grid.clear()
    chunk_grid.insert(player)
    for sprite in entity:
        chunk_grid.insert(sprite)
    for sprite in entity:
        if sprite is not player:
            dist = abs(player.x - sprite.x) + abs(player.y - sprite.y)
            if dist <   RENDER_DISTANCE:
                sprite.update(dt, chunk_grid, current_map) 
    
    player.update(chunk_grid, current_map)
        
    keys = pygame.key.get_pressed()
    player.input(keys, dt)

    for sprite in entity:
        if isinstance(sprite, ent.Grotte):
            if sprite.collides_with(player.hitbox):
                change_map()

    scalemapx, scalemapy = scale_map
    
    # CHANGEMENT : Utilisation de map.cave au lieu de map.cave_biomes

    main_map.draw(8, 8, player.position, current_map, player, cliff_edges)
    minimap_left_corner.draw(8, 8, player.position, current_map)


    drawcoeurs(10, scalemapy*32 + 16, 10)
    draw_coordinates(16, 16, player.position)
    draw_fps(16, 32)

    if keys[pygame.K_TAB]:
        minimap.draw(WINDOW_SCALE[0] // 2 - (scale_minimap*resolution_minimap)//2, 8+ (scalemapy*32) // 2 - (scale_minimap*resolution_minimap)//2, player.position, game_map)

    
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000

pygame.quit()