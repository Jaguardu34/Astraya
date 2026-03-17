import pygame
import settings
from texture import *
import world_data
from classes.items import ItemType
import render_minimap
from classes import (entity, objects)


class Minimap():
    def __init__(self, scale: int, zoom: int, screen: pygame.Surface, sprites_to_show: list) -> None:
        self.scale = scale        
        self.zoom = zoom         
        self.screen = screen
        self.sprites_to_show = sprites_to_show
        self.minimap_surface = pygame.Surface((self.scale, self.scale))
        self.distance_de_vue = 250
        self.minimap_image = pygame.image.load(render_minimap.minimap_path)

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
        self.show_hitbox = False
        self.plant_chunk_index = {}
        self.plant_chunk_size = 16
        self._cache_margin = 2
        self._highlight_surface_white = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self._highlight_surface_white, (255, 255, 255, 128), (0, 0, 32, 32), 1)
        self._highlight_surface_red = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self._highlight_surface_red, (255, 0, 0, 128), (0, 0, 32, 32), 1)
        self._last_caption_update = 0
        self.animated_positions: list[tuple[int, int, int, int, int]] = []
        self.static_cache_cx = None
        self.static_cache_cy = None
        self._init_surfaces()

    def _init_surfaces(self) -> None:
        m = self._cache_margin
        self.map_cache = pygame.Surface((self.scale_x * 32, self.scale_y * 32))
        self.static_cache = pygame.Surface(((self.scale_x + m * 2) * 32, (self.scale_y + m * 2) * 32))

    def build_plant_index(self, plant_grp, chunk_size: int = 16) -> None:
        self.plant_chunk_index = {}
        self.plant_chunk_size = chunk_size
        for plant in plant_grp:
            cx = int(plant.x // 32) // chunk_size
            cy = int(plant.y // 32) // chunk_size
            key = (cx, cy)
            if key not in self.plant_chunk_index:
                self.plant_chunk_index[key] = []
            self.plant_chunk_index[key].append(plant)

    def _draw_tile(self, surface: pygame.Surface, draw_x: int, draw_y: int, map_i: int, map_j: int, map_to_show) -> None:
        if map_i < 0 or map_j < 0 or map_j >= SIZE or map_i >= SIZE:
            pygame.draw.rect(surface, "blue", (draw_x, draw_y, 32, 32))
            return

        biome_id = map_to_show[map_j, map_i]

        if biome_id in TILE_ANIMATED:
            pygame.draw.rect(surface, "blue", (draw_x, draw_y, 32, 32))
            self.animated_positions.append((draw_x, draw_y, map_i, map_j, biome_id))
        elif biome_id in TILE_TEXTURE:
            variant = world_data.texture_variants[map_j, map_i] % len(TILE_TEXTURE[biome_id])
            surface.blit(TILE_TEXTURE[biome_id][variant], (draw_x, draw_y))
        elif biome_id in TILE_COLORS:
            pygame.draw.rect(surface, TILE_COLORS[biome_id], (draw_x, draw_y, 32, 32))
        else:
            pygame.draw.rect(surface, "blue", (draw_x, draw_y, 32, 32))

        for direction, (dj, di) in {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}.items():
            nj, ni = map_j + dj, map_i + di
            if 0 <= nj < SIZE and 0 <= ni < SIZE:
                if map_to_show[nj, ni] != biome_id:
                    edge = TILE_EDGE.get((biome_id, direction))
                    if edge:
                        surface.blit(edge, (draw_x, draw_y))

    def _blit_plants(self, tile_cx: int, tile_cy: int, map_to_show) -> None:
        if not self.plant_chunk_index:
            return
        m = self._cache_margin
        cs = self.plant_chunk_size
        cx_min = (tile_cx - self.scale_x // 2 - m) // cs
        cx_max = (tile_cx + self.scale_x // 2 + m) // cs
        cy_min = (tile_cy - self.scale_y // 2 - m) // cs
        cy_max = (tile_cy + self.scale_y // 2 + m) // cs
        origin_x = (tile_cx - self.scale_x // 2 - m) * 32
        origin_y = (tile_cy - self.scale_y // 2 - m) * 32

        for cx in range(cx_min, cx_max + 1):
            for cy in range(cy_min, cy_max + 1):
                for plant in self.plant_chunk_index.get((cx, cy), []):
                    if plant.game_map is not map_to_show:
                        continue
                    self.static_cache.blit(
                        plant.sprite[plant.texture_index],
                        (plant.x - origin_x, plant.y - origin_y)
                    )

    def _rebuild_static_cache(self, tile_cx: int, tile_cy: int, map_to_show, cliff_edges: list) -> None:
        m = self._cache_margin
        self.static_cache.fill("blue")
        self.animated_positions = []
        total_x = self.scale_x + m * 2
        total_y = self.scale_y + m * 2

        for i in range(total_x):
            for j in range(total_y):
                map_i = tile_cx - self.scale_x // 2 - m + i
                map_j = tile_cy - self.scale_y // 2 - m + j
                self._draw_tile(self.static_cache, i * 32, j * 32, map_i, map_j, map_to_show)

        self._blit_plants(tile_cx, tile_cy, map_to_show)
        self.static_cache_cx = tile_cx
        self.static_cache_cy = tile_cy

    def _scroll_cache(self, old_cx: int, old_cy: int, new_cx: int, new_cy: int, map_to_show) -> None:
        m = self._cache_margin
        dx = new_cx - old_cx
        dy = new_cy - old_cy
        shift_px = dx * 32
        shift_py = dy * 32
        self.static_cache.scroll(-shift_px, -shift_py)
        total_x = self.scale_x + m * 2
        total_y = self.scale_y + m * 2

        self.animated_positions = [
            (ax - shift_px, ay - shift_py, mi, mj, bid)
            for (ax, ay, mi, mj, bid) in self.animated_positions
        ]

        if dx > 0:
            for i in range(dx):
                col = total_x - dx + i
                map_i = new_cx + self.scale_x // 2 + m - dx + 1 + i
                for j in range(total_y):
                    self._draw_tile(self.static_cache, col * 32, j * 32, map_i, new_cy - self.scale_y // 2 - m + j, map_to_show)
        elif dx < 0:
            for i in range(-dx):
                map_i = new_cx - self.scale_x // 2 - m + i
                for j in range(total_y):
                    self._draw_tile(self.static_cache, i * 32, j * 32, map_i, new_cy - self.scale_y // 2 - m + j, map_to_show)

        if dy > 0:
            for j in range(dy):
                row = total_y - dy + j
                map_j = new_cy + self.scale_y // 2 + m - dy + 1 + j
                for i in range(total_x):
                    self._draw_tile(self.static_cache, i * 32, row * 32, new_cx - self.scale_x // 2 - m + i, map_j, map_to_show)
        elif dy < 0:
            for j in range(-dy):
                map_j = new_cy - self.scale_y // 2 - m + j
                for i in range(total_x):
                    self._draw_tile(self.static_cache, i * 32, j * 32, new_cx - self.scale_x // 2 - m + i, map_j, map_to_show)

        self._blit_plants(new_cx, new_cy, map_to_show)
        self.static_cache_cx = new_cx
        self.static_cache_cy = new_cy

    def draw(self, x: int, y: int, player_position: tuple[float, float], map_to_show, player, cliff_edges: list, mouse_pos: tuple[int, int] | None, selected_item, in_inventory: bool, block_grp) -> None:
        now = pygame.time.get_ticks()
        if now - self.anim_timer >= self.anim_speed:
            self.anim_frame = (self.anim_frame + 1) % 256
            self.anim_timer = now

        posx, posy = player_position
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)
        offset_x = int(posx % 32)
        offset_y = int(posy % 32)

        if self.static_cache_cx is None:
            self._rebuild_static_cache(tile_cx, tile_cy, map_to_show, cliff_edges)
        elif tile_cx != self.static_cache_cx or tile_cy != self.static_cache_cy:
            dx = abs(tile_cx - self.static_cache_cx)
            dy = abs(tile_cy - self.static_cache_cy)
            if dx <= 2 and dy <= 2:
                self._scroll_cache(self.static_cache_cx, self.static_cache_cy, tile_cx, tile_cy, map_to_show)
            else:
                self._rebuild_static_cache(tile_cx, tile_cy, map_to_show, cliff_edges)

        m = self._cache_margin
        self.map_cache.blit(self.static_cache, (-m * 32, -m * 32))

        for (draw_x, draw_y, map_i, map_j, biome_id) in self.animated_positions:
            frames = TILE_ANIMATED[biome_id]
            frame = (int(self.anim_frame) + world_data.texture_variants[map_j, map_i]) % len(frames)
            self.map_cache.blit(frames[frame], (draw_x - m * 32, draw_y - m * 32))

        sprites_to_draw = [
            sprite for group in self.sprites_to_show
            for sprite in group
            if sprite.game_map is map_to_show and not isinstance(sprite, objects.Plant)
        ]
        sprites_to_draw.sort(key=lambda s: s.y)

        tx, ty = 0, 0
        if mouse_pos and not in_inventory and selected_item is not None:
            if getattr(selected_item, "item_type", None) == ItemType.BLOCK:
                mouse_x, mouse_y = mouse_pos
                tx = tile_cx - self.scale_x // 2 + int((mouse_x + offset_x - x) // 32)
                ty = tile_cy - self.scale_y // 2 + int((mouse_y + offset_y - y) // 32)

        if not in_inventory and player.inventory.can_place(map_to_show, tx, ty, block_grp, player.position, entity_groups=self.sprites_to_show):
            highlight_pos = ((tx - tile_cx + self.scale_x // 2) * 32, (ty - tile_cy + self.scale_y // 2) * 32)
            self.map_cache.blit(self._highlight_surface_white, highlight_pos)

        for sprite in sprites_to_draw:
            if sprite is player:
                self.map_cache.blit(
                    player.sprite[player.texture_index],
                    (self.scale_x // 2 * 32 + offset_x, self.scale_y // 2 * 32 + offset_y)
                )
            else:
                sprite.draw(self.scale_x, self.scale_y, posx, posy, self.map_cache)

        if not in_inventory and player.inventory.can_break(map_to_show, tx, ty, block_grp, player.position):
            highlight_pos = ((tx - tile_cx + self.scale_x // 2) * 32, (ty - tile_cy + self.scale_y // 2) * 32)
            self.map_cache.blit(self._highlight_surface_red, highlight_pos)

        if self.show_hitbox:
            for sprite in sprites_to_draw:
                if hasattr(sprite, 'hitbox'):
                    for hb in sprite.hitbox:
                        pygame.draw.rect(self.map_cache, (255, 0, 0), (
                            hb.x - (tile_cx - self.scale_x // 2) * 32,
                            hb.y - (tile_cy - self.scale_y // 2) * 32,
                            hb.width, hb.height
                        ), 1)

        self.screen.blit(self.map_cache, (x - offset_x, y - offset_y))
        pygame.draw.rect(self.screen, "white", (x - 32, y - 32, self.scale_x * 32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x - 32, y + self.scale_y * 32 - 32, self.scale_x * 32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x - 32, y - 32, 32, self.scale_x * 32))
        pygame.draw.rect(self.screen, "white", (x + self.scale_x * 32 - 32, y - 32, 32, self.scale_x * 32))

    def resize(self, new_scale_x: int, new_scale_y: int) -> None:
        if new_scale_x == self.scale_x and new_scale_y == self.scale_y:
            return
        self.scale_x = new_scale_x
        self.scale_y = new_scale_y
        self._init_surfaces()
        self.static_cache_cx = None
        self.static_cache_cy = None