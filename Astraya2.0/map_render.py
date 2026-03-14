import pygame
from settings import *
from texture import *
import world_data
from classes.items import ItemType


class Minimap():
    def __init__(self, scale, zoom, screen, sprites_to_show):
        self.scale = scale        
        self.zoom = zoom         
        self.screen = screen
        self.sprites_to_show = sprites_to_show
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
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)
        

        self.minimap_surface.blit(self.get_minimap_croped(tile_cx, tile_cy), (0, 0))

        for sprite_group in self.sprites_to_show:
            for sprite in sprite_group:
                if sprite.game_map is map_to_show:
                    if sprite.show_on_minimap:
                        if abs(posx - sprite.x) < self.distance_de_vue and abs(posy - sprite.y) < self.distance_de_vue:
                            sprite.draw_minimap(self.scale / self.zoom, self.minimap_surface, tile_cx, tile_cy, self.zoom)

        pygame.draw.rect(self.screen, "orange", (x, y, self.scale + 20, self.scale + 20))
        self.screen.blit(self.minimap_surface, (x + 10, y + 10))

class Map():
    def __init__(self, scale, screen, sprites_to_show):
        self.scale_x = scale[0]
        self.scale_y = scale[1]
        self.map_cache = pygame.Surface ((self.scale_x * 32, self.scale_y  * 32))
        self.screen = screen
        self.sprites_to_show = sprites_to_show
        self.anim_timer = 0
        self.anim_frame = 0
        self.anim_speed = 300


    def draw(self, x, y, player_position, map_to_show, player, cliff_edges, mouse_pos=None, selected_item=None):
        
        sprites_to_draw = []
        
        now = pygame.time.get_ticks()
        if now - self.anim_timer >= self.anim_speed:
            self.anim_frame = (self.anim_frame + 1) % 256  # reset avant overflow
            self.anim_timer = now
        
        posx, posy = player_position  

        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)

        offset_x = (posx % 32)
        offset_y = (posy % 32)

        self.map_cache.fill("blue")
        for i in range(self.scale_x + 1):
            for j in range(self.scale_y + 1):
                map_i = tile_cx - self.scale_x//2 + i
                map_j = tile_cy - self.scale_y//2 + j

                draw_x = i * 32
                draw_y = j * 32

                
                # CHANGEMENT : map.SIZE au lieu de len(map_to_show)
                if map_i < 0 or map_j < 0 or map_j >= SIZE or map_i >= SIZE:  # Utilise map.SIZE
                    pygame.draw.rect(self.map_cache, "blue", (draw_x, draw_y, 32, 32))
                else:
                    # CHANGEMENT : Accès NumPy [y, x] et récupération de l'ID biome + variant
                    biome_id = map_to_show[map_j, map_i]  # NumPy : virgule au lieu de double crochet
                    if biome_id in TILE_ANIMATED:
                        frames = TILE_ANIMATED[biome_id]
                        offset = world_data.texture_variants[map_j, map_i] 
                        frame = (int(self.anim_frame) + offset) % len(frames)
                        self.map_cache.blit(frames[frame], (draw_x, draw_y))
                    # CHANGEMENT : Vérification de l'ID au lieu de string.startswith()
                    elif biome_id in TILE_TEXTURE:  # Vérifie l'ID numérique (1 ou 2)
                        # CHANGEMENT : Récupération du variant depuis map.texture_variants
                        variant = world_data.texture_variants[map_j, map_i] % len(TILE_TEXTURE[biome_id])  # Utilise l'array de variants
                        self.map_cache.blit(TILE_TEXTURE[biome_id][variant], (draw_x, draw_y))
                        # Tile((draw_x, draw_y), TILE_TEXTURE[biome_id][variant], tile_group)
                    elif biome_id in TILE_COLORS:  # Vérifie l'ID numérique
                        pygame.draw.rect(self.map_cache, TILE_COLORS[biome_id], (draw_x, draw_y, 32, 32))
                    else:
                        pygame.draw.rect(self.map_cache, "blue", (draw_x, draw_y, 32, 32))

                # Y a-t-il une falaise ici ?
                if (map_i, map_j) in cliff_edges:
                    biome_id = map_to_show[map_j][map_i]
                    
                    if biome_id == BIOME_IDS["cliff"]:  # ✅ CETTE LIGNE
                        for direction in cliff_edges[(map_i, map_j)]:
                                    for direction in cliff_edges[(map_i, map_j)]:
                                        texture_index = get_cliff_texture_index(map_i, map_j, direction)
                                        self.map_cache.blit(
                                            TILE_TEXTURE["cliff"][texture_index], 
                                            (draw_x, draw_y)
                                        )
        for sprite_group in self.sprites_to_show:
            for sprite in sprite_group:
                if sprite.game_map is map_to_show:
                    sprites_to_draw.append(sprite)
                    

        
        sprites_to_draw.sort(key=lambda s: s.y)
        
        highlight = None
        highlight_pos = None
        highlight_world_y = None
        if mouse_pos and selected_item is not None:
            from classes.items import ItemType
            if getattr(selected_item, "item_type", None) == ItemType.BLOCK:
                mouse_x, mouse_y = mouse_pos
                tx = tile_cx - self.scale_x // 2 + int((mouse_x + offset_x - x) // 32)
                ty = tile_cy - self.scale_y // 2 + int((mouse_y + offset_y - y) // 32)
                highlight = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (255, 255, 255, 128), (0, 0, 32, 32), 1)
                highlight_pos = (
                    (tx - tile_cx + self.scale_x // 2) * 32,
                    (ty - tile_cy + self.scale_y // 2) * 32
                )
                highlight_world_y = ty * 32  # y monde pour le tri

            highlight_drawn = False
        for sprite in sprites_to_draw:
            # dessine le highlight juste avant le joueur
            if highlight and not highlight_drawn and sprite is player:
                self.map_cache.blit(highlight, highlight_pos)
                highlight_drawn = True

            if sprite is player:
                self.map_cache.blit(
                    player.sprite[player.texture_index],
                    (self.scale_x // 2 * 32 + offset_x, self.scale_y // 2 * 32 + offset_y)
                )
            else:
                sprite.draw(self.scale_x, self.scale_y, self.map_cache, posx, posy, self.map_cache)

        if highlight and not highlight_drawn:
            self.map_cache.blit(highlight, highlight_pos)

        self.screen.blit(self.map_cache, (x - offset_x, y - offset_y))
        # bords sur screen
        pygame.draw.rect(self.screen, "white", (x-32, y-32, self.scale_x*32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x-32, y+self.scale_y*32 -32, self.scale_x*32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x-32, y-32, 32, self.scale_x*32))
        pygame.draw.rect(self.screen, "white", (x+self.scale_x*32 -32, y-32, 32, self.scale_x*32))

        