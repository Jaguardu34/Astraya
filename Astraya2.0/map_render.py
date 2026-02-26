import pygame
from settings import *
from generate_map import *


class Minimap():
    def __init__(self, scale, resolution, screen, sprite_group):
        self.scale = scale
        self.resolution = resolution
        self.screen = screen
        self.sprite_group = sprite_group
        self.minimap_surface = pygame.Surface((self.scale * self.resolution, self.scale * self.resolution))
        self.last_update_minimap = 0
        self.distance_de_vue = 250


    def draw(self, x, y, player_position, map_to_show):
        update_minimap_cooldown = 1000
        now = pygame.time.get_ticks()

        
        posx, posy = player_position
        
        tile_cx = int(posx // 16)
        tile_cy = int(posy // 16)
        
        if now-self.last_update_minimap >= update_minimap_cooldown:
            self.last_update_minimap = now
            self.minimap_surface.fill((0, 0, 255)) 
            
            for i in range(self.scale):
                for j in range(self. scale):
                    map_i = tile_cx - self.scale//2 + i
                    map_j = tile_cy - self.scale//2 + j
                    
                    # CHANGEMENT : map.SIZE au lieu de len(map_to_show)
                    if 0 <= map_j < SIZE and 0 <= map_i < SIZE:  # Utilise map.SIZE (constante) au lieu de len()
                            # CHANGEMENT : Accès NumPy [y, x] au lieu de [y][x]
                        biome_id = map_to_show[map_j, map_i]  # NumPy array : virgule au lieu de double crochet
                        color = TILE_COLORS.get(biome_id, (0, 0, 255))  # Récupère la couleur selon l'ID
                        pygame.draw.rect(self.minimap_surface, color, (i * self.resolution, j * self.resolution, self.resolution, self.resolution))

            for sprite in self.sprite_group:
                if sprite.game_map is map_to_show:
                    if sprite.show_on_minimap:
                        if abs(posx - sprite.x) < self.distance_de_vue and abs(posy - sprite.y) < self.distance_de_vue:
                            ptile_x = int(sprite.x // 16)
                            ptile_y = int(sprite.y // 16)
                            
                            rel_x = ptile_x - tile_cx + self.scale // 2
                            rel_y = ptile_y - tile_cy + self.scale // 2
                            
                            px = int(rel_x * self.resolution)
                            py = int(rel_y * self.resolution)

                            if 0 <= px < self.scale * self.resolution and 0 <= py < self.scale * self.resolution:
                                sprite.draw_minimap(self.resolution, self.minimap_surface, self.scale, tile_cx, tile_cy)

        pygame.draw.rect(self.screen, "orange", (x- self.resolution,  y- self.resolution, 
                            self.scale * self.resolution + self.resolution*2, 
                            self.scale * self.resolution + self.resolution*2))

        self.screen.blit(self.minimap_surface, (x, y))


class Map():
    def __init__(self, scale, screen, sprite_group):
        self.scale_x = scale[0]
        self.scale_y = scale[1]
        self.map_cache = pygame.Surface ((self.scale_x * 16*   SCALE, self.scale_y  * 16 *   SCALE))
        self.screen = screen
        self.sprite_group = sprite_group


    def draw(self, x, y, player_position, map_to_show, player):
        global TILE_COLORS
        
        posx, posy = player_position  

        tile_cx = int(posx // 16)
        tile_cy = int(posy // 16)

        offset_x = (posx % 16) *   SCALE
        offset_y = (posy % 16) *   SCALE

        self.map_cache.fill("blue")
        for i in range(self.scale_x + 1):
            for j in range(self.scale_y + 1):
                map_i = tile_cx - self.scale_x//2 + i
                map_j = tile_cy - self.scale_y//2 + j

                draw_x = i * 16 *   SCALE
                draw_y = j * 16 *   SCALE

                
                # CHANGEMENT : map.SIZE au lieu de len(map_to_show)
                if map_i < 0 or map_j < 0 or map_j >= SIZE or map_i >= SIZE:  # Utilise map.SIZE
                    pygame.draw.rect(self.map_cache, "blue", (draw_x, draw_y, 16*  SCALE, 16*  SCALE))
                else:
                    # CHANGEMENT : Accès NumPy [y, x] et récupération de l'ID biome + variant
                    biome_id = map_to_show[map_j, map_i]  # NumPy : virgule au lieu de double crochet
                    
                    # CHANGEMENT : Vérification de l'ID au lieu de string.startswith()
                    if biome_id in TILE_TEXTURE:  # Vérifie l'ID numérique (1 ou 2)
                        # CHANGEMENT : Récupération du variant depuis map.texture_variants
                        variant = texture_variants[map_j, map_i] % len(TILE_TEXTURE[biome_id])  # Utilise l'array de variants
                        self.map_cache.blit(TILE_TEXTURE[biome_id][variant], (draw_x, draw_y))
                        # Tile((draw_x, draw_y), TILE_TEXTURE[biome_id][variant], tile_group)
                    elif biome_id in TILE_COLORS:  # Vérifie l'ID numérique
                        pygame.draw.rect(self.map_cache, TILE_COLORS[biome_id], (draw_x, draw_y, 16*  SCALE, 16*  SCALE))
                    else:
                        pygame.draw.rect(self.map_cache, "blue", (draw_x, draw_y, 16*  SCALE, 16*  SCALE))

        for sprite in self.sprite_group:
            if sprite is not player:
                if sprite.game_map is map_to_show:
                    sprite.draw(self.scale_x, self.scale_y, self.map_cache, SCALE, posx, posy)


        self.screen.blit(self.map_cache, (x - offset_x, y - offset_y))

        # bords sur screen
        pygame.draw.rect(self.screen, "white", (x-16*  SCALE, y-16*  SCALE, self.scale_x*16*  SCALE + 32*  SCALE, 16*  SCALE))
        pygame.draw.rect(self.screen, "white", (x-16*  SCALE, y+self.scale_y*16*  SCALE -16*  SCALE, self.scale_x*16*  SCALE + 32*  SCALE, 32*  SCALE))
        pygame.draw.rect(self.screen, "white", (x-16*  SCALE, y-16*  SCALE, 16*  SCALE, self.scale_x*16*  SCALE))
        pygame.draw.rect(self.screen, "white", (x+self.scale_x*16*  SCALE -16*  SCALE, y-16*  SCALE, 32*  SCALE, self.scale_x*16*  SCALE))

        self.screen.blit(player.sprite[player.texture_index], (x + self.scale_x//2 * 16 *   SCALE, y + self.scale_y//2 * 16 *   SCALE))