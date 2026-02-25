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
#screen = pygame.display.set_mode((GAME_W * SCALE, GAME_H * SCALE), pygame.RESIZABLE)

clock = pygame.time.Clock()
running = True
dt = 0

scale_map = int(WINDOW_SCALE[0] // (16*settings.SCALE)) - 1, int(WINDOW_SCALE[1] // (16*settings.SCALE)) - 1

resolution_minimap = 4
scale_minimap = int((scale_map[1]*16*settings.SCALE) // resolution_minimap - 10)

grottes_coords = map.coord_grottes
current_world = "overworld"   # ou "cave" ou nether si on en fait un


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

grotte = ent.Grotte(texture.texture_grotte, 1530, 1530)

for i in range(nbr_poulet):
    all_sprites.add(ent.Chicken(texture.texture_chicken, random.randint(1300, 1600), random.randint(1300, 1600)))
    
all_sprites.add(player)
all_sprites.add(grotte)
#joueur    


minimap_surface = pygame.Surface((scale_minimap * resolution_minimap, scale_minimap * resolution_minimap))
last_minimap_tile = (None, None)
    
    
TILE_COLORS = {"ocean": (0, 0, 255), "jungle": (144, 238, 144),"mountains": (128, 128, 128),"snow_peak": (255, 255, 255),"forest": (0, 100, 0), "collide" : (255, 0 ,0), "beach" : (237, 201, 88), "plains" : (34, 139, 34), "rock": (50, 50, 50), "cave_normal": (120, 120, 120), "cave_mushroom": (150, 0, 150), "cave_crystal": (0, 200, 255), "cave_lava": (255, 80, 0), "cave_ice": (180, 220, 255),}
TILE_TEXTURE = {"plains" : texture.texture_herbe_upscaled, "beach" : texture.texture_sand_upscaled}
#afficher la minimap (appeler dans draw_map())    

map_decouverte = set()

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
    
    for sprite in all_sprites:
        if abs(player.x - sprite.x) < distance_de_vue and abs(player.y - sprite.y) < distance_de_vue:
            sprite.draw_minimap(x, y, resolution_minimap, screen, scale, tile_cx, tile_cy, map_decouverte)

    pygame.draw.rect(screen, "orange", (x + (scale//2 * resolution_minimap), y + (scale//2 * resolution_minimap), 4, 4))


map_cache = pygame.Surface ((scale_map[0] * 16* settings.SCALE, scale_map[1]  * 16 * settings.SCALE))
last_map_tile = (None, None)

#afficher le viewport principal
def draw_map(x, y, scalex, scaley, player_position, map_to_show):
    global last_map_tile, TILE_COLORS
    posx, posy = player_position  

    # tile centrale
    tile_cx = int(posx // 16)
    tile_cy = int(posy // 16)

    offset_x = int(posx % 16) * settings.SCALE
    offset_y = int(posy % 16) * settings.SCALE

    if (tile_cx, tile_cy) != last_map_tile:
        last_map_tile = (tile_cx, tile_cy)
        map_cache.fill("blue")
        for i in range(scalex + 1):
            for j in range(scaley + 1):
                map_i = tile_cx - scalex//2 + i
                map_j = tile_cy - scaley//2 + j

                draw_x = i * 16 * settings.SCALE
                draw_y = j * 16 * settings.SCALE

                if (tile_cx - map_i)**2 + (tile_cy - map_j)**2 < 20**2:
                    map_decouverte.add((map_i, map_j))
                    

                if map_i < 0 or map_j < 0 or map_j >= len(map_to_show) or map_i >= len(map_to_show[map_j]):
                    pygame.draw.rect(map_cache, "blue", (draw_x, draw_y, 16*settings.SCALE, 16*settings.SCALE))
                else:
                    tile = map_to_show[map_j][map_i]
                    tile_base = tile.split("*")[0]
                    if tile_base in TILE_TEXTURE:
                        index = tile_index_cache.get((map_i, map_j), 0)
                        map_cache.blit(TILE_TEXTURE[tile_base][index], (draw_x, draw_y))
                    elif tile in TILE_COLORS:
                        pygame.draw.rect(map_cache, TILE_COLORS[tile], (draw_x, draw_y, 16*settings.SCALE, 16*settings.SCALE))
                    else:
                        pygame.draw.rect(map_cache, "blue", (draw_x, draw_y, 16*settings.SCALE, 16*settings.SCALE))
    screen.blit(map_cache, (x - offset_x, y - offset_y))
    # ===== 2. DESSINER LES GROTTES =====
    for grotte_x, grotte_y in grottes_coords:
        # Position de la grotte par rapport à la caméra
        gx = x + (grotte_x * 16 - (tile_cx - scalex//2) * 16) * settings.SCALE - offset_x
        gy = y + (grotte_y * 16 - (tile_cy - scaley//2) * 16) * settings.SCALE - offset_y

        # Ne dessiner que si visible à l'écran
        if -16*settings.SCALE <= gx < (scalex+1)*16*settings.SCALE and -16*settings.SCALE <= gy < (scaley+1)*16*settings.SCALE:
            
            # Rectangle temporaire (jaune pour les voir facilement)
            pygame.draw.rect(screen, "pink", (int(gx), int(gy), 16*settings.SCALE, 16*settings.SCALE))
            pygame.draw.circle(screen, "black", (int(gx + 8*settings.SCALE), int(gy + 8*settings.SCALE)), 4*settings.SCALE)


    for sprite in all_sprites:
        if sprite is not player:
            sprite.draw(x, y, scalex, scaley, screen, settings.SCALE, posx, posy)

    # bords sur screen, avec coordonnées écran
    pygame.draw.rect(screen, "white", (x-16*settings.SCALE, y-16*settings.SCALE, scalex*16*settings.SCALE + 32*settings.SCALE, 16*settings.SCALE))
    pygame.draw.rect(screen, "white", (x-16*settings.SCALE, y+scaley*16*settings.SCALE -16*settings.SCALE, scalex*16*settings.SCALE + 32*settings.SCALE, 32*settings.SCALE))
    pygame.draw.rect(screen, "white", (x-16*settings.SCALE, y-16*settings.SCALE, 16*settings.SCALE, scalex*16*settings.SCALE))
    pygame.draw.rect(screen, "white", (x+scalex*16*settings.SCALE -16*settings.SCALE, y-16*settings.SCALE, 32*settings.SCALE, scalex*16*settings.SCALE))

    screen.blit(player.sprite[player.texture_index], (x + scalex//2 * 16 * settings.SCALE, y + scaley//2 * 16 * settings.SCALE))
    

  
#afficher les coeurs
def drawcoeurs(x, y, nbcoeurs):
    for i in range(nbcoeurs):
        screen.blit(texture.texture_coeur_upscaled, (x + (i*(texture.texture_coeur_upscaled.get_width()+8)), y))
                    

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

#boucle de jeu
while running:
    #quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    scalemapx, scalemapy = scale_map
    if current_world == "overworld":
        draw_map(4*settings.SCALE, 4*settings.SCALE, scalemapx, scalemapy, player.get_pos(), map.map)
    else:
        draw_map(4*settings.SCALE, 4*settings.SCALE, scalemapx, scalemapy, player.get_pos(), map.cave_biomes)

    
    drawcoeurs(10, scalemapy*16*settings.SCALE + 16, 10)
    
    draw_coordinates(8*settings.SCALE, 8*settings.SCALE, player.get_pos())
    
    draw_fps(8*settings.SCALE, 16*settings.SCALE)
    
    for sprite in all_sprites:
        if sprite is not player:
            dist = abs(player.x - sprite.x) + abs(player.y - sprite.y)  # manhattan, plus rapide que sqrt
            if dist < settings.RENDER_DISTANCE:
                sprite.update(dt, chunk_grid, player.x, player.y) 
    
    chunk_grid.clear()
    chunk_grid.insert(player)
    for sprite in all_sprites:
        chunk_grid.insert(sprite)
    
    player.update()
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB]:
        draw_minimap(WINDOW_SCALE[0] // 2 - (scale_minimap*resolution_minimap)//2, (4*settings.SCALE)+ (scalemapy*16*settings.SCALE) // 2 - (scale_minimap*resolution_minimap)//2, scale_minimap, player.get_pos(), map.map)
    player.input(keys, dt, chunk_grid)

    for sprite in all_sprites:
        if isinstance(sprite, ent.Object):
            if sprite.collides_with(player.collide_box):
                change_map()

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

