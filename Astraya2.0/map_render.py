import pygame
import settings
from texture import *
import world_data
from classes.items import ItemType
import render_minimap
import entity


class Minimap():
    def __init__(self, scale: int, zoom: int, screen: pygame.Surface, sprites_to_show: list) -> None:
        self.scale = scale        
        self.zoom = zoom         
        self.screen = screen
        self.sprites_to_show = sprites_to_show
        self.minimap_surface = pygame.Surface((self.scale, self.scale))
        self.distance_de_vue = 250
        self.minimap_image = pygame.image.load(render_minimap.minimap_pathhttps://github.com/Jaguardu34/Astraya)

    def get_minimap_croped(self, tile_cx: int, tile_cy: int) -> pygame.Surface:
        src_x = tile_cx - self.zoom // 2
        src_y = tile_cy - self.zoom // 2
        minimap_croped = pygame.Surface((self.zoom, self.zoom), pygame.SRCALPHA)
        minimap_croped.blit(self.minimap_image, (0, 0), (src_x, src_y, self.zoom, self.zoom))
        minimap_croped_upscaled = pygame.transform.scale(minimap_croped, (self.scale, self.scale))
        return minimap_croped_upscaled

    def draw(self, x: int, y: int, player_position: tuple[float, float], map_to_show) -> None:
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
    def __init__(self, scale: tuple[int, int], screen: pygame.Surface, sprites_to_show: list) -> None:
        self.scale_x = scale[0]
        self.scale_y = scale[1]
        self.screen = screen
        self.sprites_to_show = sprites_to_show
        self.anim_timer = 0
        self.anim_frame = 0
        self.anim_speed = 500
        self.map_cache = pygame.Surface((self.scale_x * 32, self.scale_y * 32))
        self.static_cache = pygame.Surface(((self.scale_x + 2) * 32, (self.scale_y + 2) * 32))
        self.static_cache_cx = None
        self.static_cache_cy = None
        self.animated_positions: list[tuple[int, int, int, int, int]] = []
        self.show_hitbox = False

    def _rebuild_static_cache(self, tile_cx: int, tile_cy: int, map_to_show, cliff_edges: list) -> None:
        self.static_cache.fill("blue")
        self.animated_positions = []

        for i in range(self.scale_x + 2):
            for j in range(self.scale_y + 2):
                map_i = tile_cx - self.scale_x // 2 - 1 + i
                map_j = tile_cy - self.scale_y // 2 - 1 + j
                draw_x = i * 32
                draw_y = j * 32

                if map_i < 0 or map_j < 0 or map_j >= SIZE or map_i >= SIZE:
                    pygame.draw.rect(self.static_cache, "blue", (draw_x, draw_y, 32, 32))
                    continue

                biome_id = map_to_show[map_j, map_i]

                if biome_id in TILE_ANIMATED:
                    pygame.draw.rect(self.static_cache, "blue", (draw_x, draw_y, 32, 32))
                    self.animated_positions.append((draw_x, draw_y, map_i, map_j, biome_id))
                elif biome_id in TILE_TEXTURE:
                    variant = world_data.texture_variants[map_j, map_i] % len(TILE_TEXTURE[biome_id])
                    self.static_cache.blit(TILE_TEXTURE[biome_id][variant], (draw_x, draw_y))
                elif biome_id in TILE_COLORS:
                    pygame.draw.rect(self.static_cache, TILE_COLORS[biome_id], (draw_x, draw_y, 32, 32))
                else:
                    pygame.draw.rect(self.static_cache, "blue", (draw_x, draw_y, 32, 32))

        self.static_cache_cx = tile_cx
        self.static_cache_cy = tile_cy
        
        for sprite_group in self.sprites_to_show:
            for sprite in sprite_group:
                if isinstance(sprite, entity.Plant) and sprite.game_map is map_to_show:
                    draw_x = sprite.x - (tile_cx - self.scale_x // 2 - 1) * 32
                    draw_y = sprite.y - (tile_cy - self.scale_y // 2 - 1) * 32
                    if -32 <= draw_x < (self.scale_x + 2) * 32 and -32 <= draw_y < (self.scale_y + 2) * 32:
                        self.static_cache.blit(sprite.sprite[sprite.texture_index], (draw_x, draw_y))

    def draw(self, x: int, y: int, player_position: tuple[float, float], map_to_show, player, cliff_edges: list, mouse_pos: tuple[int, int] | None, selected_item, in_inventory: bool, block_grp) -> None:
        sprites_to_draw: list = []

        now = pygame.time.get_ticks()
        if now - self.anim_timer >= self.anim_speed:
            self.anim_frame = (self.anim_frame + 1) % 256
            self.anim_timer = now

        posx, posy = player_position
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)
        offset_x = int(posx % 32)
        offset_y = int(posy % 32)

        if tile_cx != self.static_cache_cx or tile_cy != self.static_cache_cy:
            self._rebuild_static_cache(tile_cx, tile_cy, map_to_show, cliff_edges)

        self.map_cache.blit(self.static_cache, (-32, -32))

        for (draw_x, draw_y, map_i, map_j, biome_id) in self.animated_positions:
            frames = TILE_ANIMATED[biome_id]
            offset = world_data.texture_variants[map_j, map_i]
            frame = (int(self.anim_frame) + offset) % len(frames)
            self.map_cache.blit(frames[frame], (draw_x - 32, draw_y - 32))


                    
        for sprite_group in self.sprites_to_show:
            for sprite in sprite_group:
                if sprite.game_map is map_to_show and not isinstance(sprite, entity.Plant):
                    sprites_to_draw.append(sprite)

        sprites_to_draw.sort(key=lambda s: s.y)

        highlight = None
        highlight_pos: tuple[int, int] | None = None
        tx, ty = 0, 0

        if mouse_pos and selected_item is not None:
            if getattr(selected_item, "item_type", None) == ItemType.BLOCK:
                mouse_x, mouse_y = mouse_pos
                tx = tile_cx - self.scale_x // 2 + int((mouse_x + offset_x - x) // 32)
                ty = tile_cy - self.scale_y // 2 + int((mouse_y + offset_y - y) // 32)
                

        if not in_inventory and player.inventory.can_place(map_to_show, tx, ty, block_grp, player.position, entity_groups=self.sprites_to_show):
            highlight = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.rect(highlight, (255, 255, 255, 128), (0, 0, 32, 32), 1)
            highlight_pos = (
                (tx - tile_cx + self.scale_x // 2) * 32,
                (ty - tile_cy + self.scale_y // 2) * 32
            )
            self.map_cache.blit(highlight, highlight_pos)
         
           

        for sprite in sprites_to_draw:
            if sprite is player:
                self.map_cache.blit(
                    player.sprite[player.texture_index],
                    (self.scale_x // 2 * 32 + offset_x, self.scale_y // 2 * 32 + offset_y)
                )
            else:
                sprite.draw(self.scale_x, self.scale_y, self.map_cache, posx, posy, self.map_cache)
                
        if not in_inventory and player.inventory.can_break(map_to_show, tx, ty, block_grp, player.position):
            highlight = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.rect(highlight, (255, 0, 0, 128), (0, 0, 32, 32), 1)
            highlight_pos = (
                (tx - tile_cx + self.scale_x // 2) * 32,
                (ty - tile_cy + self.scale_y // 2) * 32
            )
            self.map_cache.blit(highlight, highlight_pos)
                
        #debug pr afficher hitbox
        if self.show_hitbox:
            for sprite in sprites_to_draw:
                if hasattr(sprite, 'hitbox'):
                    for hb in sprite.hitbox:
                        # convertir world coords → screen coords
                        draw_hb_x = hb.x - (tile_cx - self.scale_x//2) * 32
                        draw_hb_y = hb.y - (tile_cy - self.scale_y//2) * 32
                        pygame.draw.rect(self.map_cache, (255, 0, 0), (draw_hb_x, draw_hb_y, hb.width, hb.height), 1)
                        
        


        self.screen.blit(self.map_cache, (x - offset_x, y - offset_y))
            
        pygame.draw.rect(self.screen, "white", (x - 32, y - 32, self.scale_x * 32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x - 32, y + self.scale_y * 32 - 32, self.scale_x * 32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x - 32, y - 32, 32, self.scale_x * 32))
        pygame.draw.rect(self.screen, "white", (x + self.scale_x * 32 - 32, y - 32, 32, self.scale_x * 32))
