#Classes pour affichage de la map et minimap

#Imports
import pygame
from texture import *
import world_data
from classes.items import ItemType
import render_minimap
from classes import (objects)

#class minimap
class Minimap():
    #init variables
    def __init__(self, scale: int, zoom: int, screen: pygame.Surface, sprites_to_show: list) -> None:
        self.scale = scale        
        self.zoom = zoom         
        self.screen = screen
        self.sprites_to_show = sprites_to_show
        self.minimap_surface = pygame.Surface((self.scale, self.scale))
        self.distance_de_vue = 250
        self.minimap_image = pygame.image.load(render_minimap.minimap_path)

    #recuperer la minimap.png coupée pr afficher le bon endroit
    def get_minimap_croped(self, tile_cx: int, tile_cy: int) -> pygame.Surface:
        src_x = tile_cx - self.zoom // 2
        src_y = tile_cy - self.zoom // 2
        minimap_croped = pygame.Surface((self.zoom, self.zoom), pygame.SRCALPHA)
        minimap_croped.blit(self.minimap_image, (0, 0), (src_x, src_y, self.zoom, self.zoom))
        minimap_croped_upscaled = pygame.transform.scale(minimap_croped, (self.scale, self.scale))
        return minimap_croped_upscaled

    #afficher la minimap a l'écran
    def draw(self, x: int, y: int, player_position: tuple[float, float], map_to_show) -> None:
        #transformer pos joueur en pos tile
        posx, posy = player_position
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)
        
        #creer la surface de la minimap
        self.minimap_surface.blit(self.get_minimap_croped(tile_cx, tile_cy), (0, 0))

        #afficher les entitées
        for sprite_group in self.sprites_to_show:
            for sprite in sprite_group:
                if sprite.game_map is map_to_show:
                    if sprite.show_on_minimap:
                        if abs(posx - sprite.x) < self.distance_de_vue and abs(posy - sprite.y) < self.distance_de_vue:
                            sprite.draw_minimap(self.scale / self.zoom, self.minimap_surface, tile_cx, tile_cy, self.zoom)

        #afficher la minimap avec bords oranges
        pygame.draw.rect(self.screen, "orange", (x, y, self.scale + 20, self.scale + 20))
        self.screen.blit(self.minimap_surface, (x + 10, y + 10))

#class map principale
class Map():
    #init variables
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

    #init surface principale avec cache pr performances
    def _init_surfaces(self) -> None:
        m = self._cache_margin
        self.map_cache = pygame.Surface((self.scale_x * 32, self.scale_y * 32))
        self.static_cache = pygame.Surface(((self.scale_x + m * 2) * 32, (self.scale_y + m * 2) * 32))

    #creer l'emplacement des plantes et le garder en memoire dans un tableau
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

    #afficher les tiles du fond ou couleur si pas de texture
    def _draw_tile(self, surface: pygame.Surface, draw_x: int, draw_y: int, map_i: int, map_j: int, map_to_show) -> None:
        if map_i < 0 or map_j < 0 or map_j >= map_to_show.shape[0] or map_i >= map_to_show.shape[1]:
            pygame.draw.rect(surface, "blue", (draw_x, draw_y, 32, 32))
            return
        
        #recuperer l'id du biome de la tile
        biome_id = map_to_show[map_j, map_i]

        #animer tile si animée
        if biome_id in TILE_ANIMATED:
            pygame.draw.rect(surface, "blue", (draw_x, draw_y, 32, 32))
            self.animated_positions.append((draw_x, draw_y, map_i, map_j, biome_id))
        #si texture afficher texture
        elif biome_id in TILE_TEXTURE:
            variant = world_data.texture_variants[map_j, map_i] % len(TILE_TEXTURE[biome_id])
            surface.blit(TILE_TEXTURE[biome_id][variant], (draw_x, draw_y))
        #sinon couleur
        elif biome_id in TILE_COLORS:
            pygame.draw.rect(surface, TILE_COLORS[biome_id], (draw_x, draw_y, 32, 32))
        #ou sinon dernier recour bleu pr pas crash
        else:
            pygame.draw.rect(surface, "blue", (draw_x, draw_y, 32, 32))

        #afficher les bords des biomes
        for direction, (dj, di) in {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}.items():
            nj, ni = map_j + dj, map_i + di
            h, w = map_to_show.shape
            if 0 <= nj < h and 0 <= ni < w:
                if map_to_show[nj, ni] != biome_id:
                    edge = TILE_EDGE.get((biome_id, direction))
                    if edge:
                        surface.blit(edge, (draw_x, draw_y))

    #afficher les plantes en fonction du tab crée plus tot
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

                    px = plant.x - origin_x
                    py = plant.y - origin_y

                    if px < -32 or py < -32 or px > self.static_cache.get_width() or py > self.static_cache.get_height():
                        continue

                    self.static_cache.blit(
                        plant.sprite[plant.texture_index],(px, py))

    def _rebuild_static_cache(self, tile_cx: int, tile_cy: int, map_to_show, cliff_edges: list, is_dungeon) -> None:
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

        if not is_dungeon:
            self._blit_plants(tile_cx, tile_cy, map_to_show)
        self.static_cache_cx = tile_cx
        self.static_cache_cy = tile_cy

    def _scroll_cache(self, old_cx, old_cy, new_cx, new_cy, map_to_show, is_dungeon):
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

        if not is_dungeon:
            self._blit_plants(new_cx, new_cy, map_to_show)
        self.static_cache_cx = new_cx
        self.static_cache_cy = new_cy

    #afficher la map
    def draw(self, x: int, y: int, player_position: tuple[float, float], map_to_show, player, cliff_edges: list, mouse_pos: tuple[int, int] | None, selected_item, in_inventory: bool, block_grp) -> None:
        now = pygame.time.get_ticks()
        is_dungeon = map_to_show.shape[0] < 300

        if now - self.anim_timer >= self.anim_speed:
            self.anim_frame = (self.anim_frame + 1) % 256
            self.anim_timer = now

        # Position du joueur (celle passée par Game, cohérente avec le rendu)
        posx, posy = player_position
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)

        # Offset pixel à l'intérieur de la tuile centrale
        # IMPORTANT : basé sur player_position, pas sur player.x / player.y
        offset_x = int(posx % 32)
        offset_y = int(posy % 32)

        # Gestion du cache statique
        if self.static_cache_cx is None:
            self._rebuild_static_cache(tile_cx, tile_cy, map_to_show, cliff_edges, is_dungeon)
        elif tile_cx != self.static_cache_cx or tile_cy != self.static_cache_cy:
            dx = abs(tile_cx - self.static_cache_cx)
            dy = abs(tile_cy - self.static_cache_cy)
            if dx <= 2 and dy <= 2:
                self._scroll_cache(self.static_cache_cx, self.static_cache_cy, tile_cx, tile_cy, map_to_show, is_dungeon)
            else:
                self._rebuild_static_cache(tile_cx, tile_cy, map_to_show, cliff_edges, is_dungeon)

        m = self._cache_margin
        self.map_cache.blit(self.static_cache, (-m * 32, -m * 32))

        # Tuiles animées
        for (draw_x, draw_y, map_i, map_j, biome_id) in self.animated_positions:
            frames = TILE_ANIMATED[biome_id]
            frame = (int(self.anim_frame) + world_data.texture_variants[map_j, map_i]) % len(frames)
            self.map_cache.blit(frames[frame], (draw_x - m * 32, draw_y - m * 32))

        # Sprites
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

        # Highlight placement
        if not in_inventory and player.inventory.can_place(map_to_show, tx, ty, block_grp, player.position, entity_groups=self.sprites_to_show):
            highlight_pos = ((tx - tile_cx + self.scale_x // 2) * 32,
                            (ty - tile_cy + self.scale_y // 2) * 32)
            self.map_cache.blit(self._highlight_surface_white, highlight_pos)

        #afficher les entités
        # Dessin des sprites
        for sprite in sprites_to_draw:
            if sprite is player:
                # Le joueur est toujours centré dans la map_cache, avec l'offset fin
                self.map_cache.blit(
                    player.sprite[player.texture_index],
                    (self.scale_x // 2 * 32 + offset_x,
                    self.scale_y // 2 * 32 + offset_y)
                )
            else:
                sprite.draw(self.scale_x, self.scale_y, posx, posy, self.map_cache)

        #afficher le highlight des blocs
        # Highlight break
        if not in_inventory and player.inventory.can_break(map_to_show, tx, ty, block_grp, player.position):
            highlight_pos = ((tx - tile_cx + self.scale_x // 2) * 32,
                            (ty - tile_cy + self.scale_y // 2) * 32)
            self.map_cache.blit(self._highlight_surface_red, highlight_pos)

        # Hitbox debug
        if self.show_hitbox:
            for sprite in sprites_to_draw:
                if hasattr(sprite, 'hitbox'):
                    for hb in sprite.hitbox:
                        pygame.draw.rect(
                            self.map_cache,
                            (255, 0, 0),
                            (
                                hb.x - (tile_cx - self.scale_x // 2) * 32,
                                hb.y - (tile_cy - self.scale_y // 2) * 32,
                                hb.width,
                                hb.height
                            ),
                            1
                        )

        # Blit final : on applique l'offset pixel fin
        self.screen.blit(self.map_cache, (x - offset_x, y - offset_y))

        # Bordures blanches
        pygame.draw.rect(self.screen, "white", (x - 32, y - 32, self.scale_x * 32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x - 32, y + self.scale_y * 32 - 32, self.scale_x * 32 + 32, 32))
        pygame.draw.rect(self.screen, "white", (x - 32, y - 32, 32, self.scale_x * 32))
        pygame.draw.rect(self.screen, "white", (x + self.scale_x * 32 - 32, y - 32, 32, self.scale_x * 32))

    #fonction pr resize la map si besoin
    def resize(self, new_scale_x: int, new_scale_y: int) -> None:
        if new_scale_x == self.scale_x and new_scale_y == self.scale_y:
            return
        self.scale_x = new_scale_x
        self.scale_y = new_scale_y
        self._init_surfaces()
        self.static_cache_cx = None
        self.static_cache_cy = None