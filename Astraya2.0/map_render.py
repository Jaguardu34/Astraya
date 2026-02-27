import pygame
from settings import *
from generate_map import *
from texture import *
import render_minimap


class Minimap():
    def __init__(self, scale, zoom, screen, sprite_group):
        self.scale = scale        
        self.zoom = zoom         
        self.screen = screen
        self.sprite_group = sprite_group
        self.minimap_surface = pygame.Surface((self.scale, self.scale))
        self.distance_de_vue = 250
        self.minimap_image = pygame.image.load(TEXTURE_MINIMAP_PATH)

    def get_minimap_croped(self, tile_cx, tile_cy):
        src_x = tile_cx - self.zoom // 2
        src_y = tile_cy - self.zoom // 2
        minimap_croped = pygame.Surface((self.zoom, self.zoom), pygame.SRCALPHA)
        minimap_croped.blit(self.minimap_image, (0, 0), (src_x, src_y, self.zoom, self.zoom))
        minimap_croped_upscaled = pygame.transform.scale(minimap_croped, (self.scale, self.scale))
        return minimap_croped_upscaled

    def draw(self, x, y, player_position, map_to_show):
        posx, posy = player_position
        tile_cx = int(posx // 16)
        tile_cy = int(posy // 16)
        

        self.minimap_surface.blit(self.get_minimap_croped(tile_cx, tile_cy), (0, 0))

        for sprite in self.sprite_group:
            if sprite.game_map is map_to_show:
                if sprite.show_on_minimap:
                    if abs(posx - sprite.x) < self.distance_de_vue and abs(posy - sprite.y) < self.distance_de_vue:
                        sprite.draw_minimap(self.scale / self.zoom, self.minimap_surface, self.zoom, tile_cx, tile_cy)

        pygame.draw.rect(self.screen, "orange", (x, y, self.scale + 20, self.scale + 20))
        self.screen.blit(self.minimap_surface, (x + 10, y + 10))

class Map():
    def __init__(self, scale, screen, sprite_group):
        self.scale_x = scale[0]
        self.scale_y = scale[1]
        self.map_cache = pygame.Surface ((self.scale_x * 16*   SCALE, self.scale_y  * 16 *   SCALE))
        self.screen = screen
        self.sprite_group = sprite_group


    def draw(self, x, y, player_position, map_to_show, player, cliff_edges):
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

                # Y a-t-il une falaise ici ?
                if (map_i, map_j) in cliff_edges.keys():
                    for direction in cliff_edges[(map_i, map_j)]:
                        # Dessiner le sprite de falaise correspondant
                        pygame.draw.rect(self.map_cache, "pink", (draw_x, draw_y, 16*  SCALE, 16*  SCALE))

        #self.screen.blit(self.minimap_surface, (x, y))


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