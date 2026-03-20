import random
import pygame
import settings
import math
import texture
from classes.inventory import Inventory

def get_rect(x, y, size=12):
    return pygame.Rect(x - size//2, y - size//2, size, size)

def check_collision_entites(ax, ay, bx, by, size=32):
    return pygame.Rect(ax, ay, size, size).colliderect(pygame.Rect(bx, by, size, size))

def check_box_collide(box1, box2):
    if len(box1) == 1 and len(box2) == 1:
        return box1[0].colliderect(box2[0])
    for r1 in box1:
        for r2 in box2:
            if r1.colliderect(r2):
                return True
    return False

def veriftile(x, y, game_map, altitude_map=None, current_altitude=0):
    if x < 0 or y < 0 or y >= settings.SIZE or x >= settings.SIZE:
        return "ocean"
    biome_id = game_map[y, x]
    if biome_id in settings.COLLIDE_TILES:
        return biome_id
    return True

def calculate_hitbox_size(sprite, shrink=2):
    surf = sprite[0]
    bounding = surf.get_bounding_rect()
    size = min(bounding.width, bounding.height) - shrink
    return max(4, size), bounding.x, bounding.y

def veriftile_pixel(px, py, game_map, altitude_map=None, current_altitude=0, size=32):
    corners = [
        (px,          py),
        (px + size-1, py),
        (px,          py + size-1),
        (px + size-1, py + size-1),
    ]
    for cx, cy in corners:
        result = veriftile(int(cx // 32), int(cy // 32), game_map, altitude_map, current_altitude)
        if result is not True:
            return result
    return True


class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500):
        super().__init__()
        self.x = float(x * 32)
        self.y = float(y * 32)
        self.tile_x = x
        self.tile_y = y
        self.sprite = sprite
        self.sprite_minimap = []
        self.texture_index = 0
        self.image = self.sprite[self.texture_index]
        self.rect = self.image.get_rect(topleft=(x * 32, y * 32))
        self.generate_minimap_sprite()
        self.game_map = game_map
        self.altitude_map = altitude_map
        self.actual_map = game_map
        self.is_static = False
        self.hitbox_size, self.hitbox_offset_x, self.hitbox_offset_y = calculate_hitbox_size(sprite)

        if altitude_map is not None:
            self.altitude = altitude_map[int(y), int(x)]
        else:
            self.altitude = 0
        
        # Dans Entity.__init__, temporairement :

    def update_altitude(self):
        if self.altitude_map is not None:
            tile_x = int(self.x // 32)
            tile_y = int(self.y // 32)
            if 0 <= tile_x < settings.SIZE and 0 <= tile_y < settings.SIZE:
                self.altitude = self.altitude_map[tile_y, tile_x]

    def update(self, actual_map):
        self.texture_index = self.texture_index % len(self.sprite)
        self.actual_map = actual_map

    def generate_minimap_sprite(self):
        for i in range(len(self.sprite)):
            self.sprite_minimap.append(pygame.transform.scale(self.sprite[i], (self.sprite[i].get_width() // 2, self.sprite[i].get_height() // 2)))

    def draw(self, scalex, scaley, posx, posy, surface):
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)
        px = (self.x - (tile_cx - scalex//2) * 32)
        py = (self.y - (tile_cy - scaley//2) * 32)
        if 0 <= px < scalex*32 and 0 <= py < scaley*32:
            surface.blit(self.sprite[self.texture_index], (px, py))

    def draw_minimap(self, resolution_minimap, screen, tile_cx, tile_cy, zoom):
        ptile_x = int(self.x // 32)
        ptile_y = int(self.y // 32)
        rel_x = ptile_x - tile_cx + zoom // 2
        rel_y = ptile_y - tile_cy + zoom // 2
        px = int(rel_x * resolution_minimap)
        py = int(rel_y * resolution_minimap)
        texture = self.sprite_minimap[self.texture_index]
        px -= texture.get_width() // 2
        py -= texture.get_height() // 2
        screen.blit(texture, (px, py))

    @property
    def position(self):
        return (self.x, self.y)

    def check_collision_with_group(self, group):
        for entity in group:
            if entity is self:
                continue
            if hasattr(entity, 'hitbox'):
                if check_box_collide(self.hitbox, entity.hitbox):
                    return entity
        return False


class Entity_That_Move_And_Has_Collision(Entity):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.hitbox = [pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_size, self.hitbox_size
        )]
        self.has_hitbox = True
        self.vx = 0
        self.vy = 0

    def update(self, chunk_grid, actual_map):
        self.hitbox[0].x = self.x + self.hitbox_offset_x
        self.hitbox[0].y = self.y + self.hitbox_offset_y

        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            new_x = self.x + self.vx
            new_y = self.y + self.vy

            nearby = chunk_grid.get_nearby(new_x, new_y)
            w = self.hitbox[0].width
            h = self.hitbox[0].height

            rect_x = [pygame.Rect(new_x + self.hitbox_offset_x, self.y + self.hitbox_offset_y, w, h)]
            rect_y = [pygame.Rect(self.x + self.hitbox_offset_x, new_y + self.hitbox_offset_y, w, h)]

            if veriftile_pixel(new_x + self.hitbox_offset_x, self.y + self.hitbox_offset_y, self.actual_map, self.altitude_map, self.altitude, self.hitbox_size) is True:
                blocked = False
                for p in nearby:
                    if p.game_map is not self.actual_map: continue
                    if p is self: continue
                    if p.is_static:
                        if p.has_hitbox and check_box_collide(p.hitbox, rect_x):
                            blocked = True
                            if self.vx > 0:
                                self.x = p.hitbox[0].left - w - self.hitbox_offset_x
                            else:
                                self.x = p.hitbox[0].right - self.hitbox_offset_x
                            self.vx = 0
                            break
                    elif p.has_hitbox and check_box_collide(p.hitbox, rect_x):
                        if veriftile_pixel(p.x + self.vx + p.hitbox_offset_x, p.y + p.hitbox_offset_y, self.actual_map, self.altitude_map, self.altitude, p.hitbox_size) is True:
                            p.vx += self.vx * 1.05
                        blocked = True
                        break
                if not blocked:
                    self.x = new_x

            if veriftile_pixel(self.x + self.hitbox_offset_x, new_y + self.hitbox_offset_y, self.actual_map, self.altitude_map, self.altitude, self.hitbox_size) is True:
                blocked = False
                for p in nearby:
                    if p.game_map is not self.actual_map: continue
                    if p is self: continue
                    if p.is_static:
                        if p.has_hitbox and check_box_collide(p.hitbox, rect_y):
                            blocked = True
                            if self.vy > 0:
                                self.y = p.hitbox[0].top - h - self.hitbox_offset_y
                            else:
                                self.y = p.hitbox[0].bottom - self.hitbox_offset_y
                            self.vy = 0
                            break
                    elif p.has_hitbox and check_box_collide(p.hitbox, rect_y):
                        if veriftile_pixel(p.x + p.hitbox_offset_x, p.y + self.vy + p.hitbox_offset_y, self.actual_map, self.altitude_map, self.altitude, p.hitbox_size) is True:
                            p.vy += self.vy * 1.05
                        blocked = True
                        break
                if not blocked:
                    self.y = new_y

            self.vx *= 0.8
            self.vy *= 0.8

        self.update_altitude()
        super().update(actual_map)

    def move(self, dx, dy):
        self.vx += dx
        self.vy += dy







class Object(Entity):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.is_static = True

    def update(self, dt, chunk_grid, actual_map):
        super().update(actual_map)


class Projectile(Entity):
    def __init__(self, sprite, game_map, launcher, direction=90, speed=10, altitude_map=None, x=0, y=0):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.hitbox = [pygame.Rect(self.x, self.y, sprite[0].get_width() // 2, sprite[0].get_height() // 2)]
        self.has_hitbox = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 20000
        self.update_hitbox_cooldown = 100
        self.last_update_hitbox = pygame.time.get_ticks()
        self.launcher = launcher

    def angle_to_vector(self, angle_deg):
        angle_rad = math.radians(angle_deg)
        x = math.cos(angle_rad)
        y = math.sin(angle_rad)
        return (x * 0.1, y * 0.1)

    def update(self, actual_map):
        super().update(actual_map)
        now = pygame.time.get_ticks()
        vx, vy = self.angle_to_vector(self.direction)
        self.x += vx * self.speed
        self.y += vy * self.speed

        if veriftile_pixel(self.x, self.y, self.actual_map, self.altitude_map, self.altitude) is not True:
            self.kill()
            return

        if now - self.last_update_hitbox >= self.update_hitbox_cooldown:
            self.last_update_hitbox = now
            self.hitbox[0].x = self.x
            self.hitbox[0].y = self.y
        if now - self.spawn_time >= self.lifetime:
            self.kill()
            return





class DroppedItem(pygame.sprite.Sprite):
    def __init__(self, x_px, y_px, item, quantity, game_map):
        super().__init__()
        self.x = float(x_px)
        self.y = float(y_px)
        self.item = item
        self.quantity = quantity
        self.game_map = game_map
        self.actual_map = game_map
        self.show_on_minimap = False
        self.is_static = True
        self.has_hitbox = True
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0
        self.image = pygame.Surface((20, 20))
        self.image.fill((139, 90, 43))
        pygame.draw.rect(self.image, (80, 50, 20), (0, 0, 20, 20), 2)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hitbox = [pygame.Rect(self.x - 12, self.y - 12, 24, 24)]

    def draw(self, scalex, scaley, screen, posx, posy):
        tile_cx = int(posx // 32)
        tile_cy = int(posy // 32)
        px = (self.x - (tile_cx - scalex//2) * 32)
        py = (self.y - (tile_cy - scaley//2) * 32)
        if -32 <= px < scalex*32 + 32 and -32 <= py < scaley*32 + 32:
            screen.blit(self.image, (px - 10, py - 10))

    def update(self, dt, chunk_grid, actual_map):
        self.actual_map = actual_map
        self.hitbox[0].x = self.x - 12
        self.hitbox[0].y = self.y - 12
        


class DungeonDoor(Entity):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500):
        super().__init__(sprite, game_map, altitude_map, x, y)

        self.show_on_minimap = False
        self.has_hitbox = True
        self.hitbox = [pygame.Rect(self.x, self.y, 32, 32)]
        self.vx = 0
        self.vy = 0

        self.interact_zone = pygame.Rect(
            self.x - 48,   # 1.5 blocs à gauche
            self.y - 48,   # 1.5 blocs au-dessus
            96,            # 3 blocs de large
            96             # 3 blocs de haut
        )

    def player_can_enter(self, player_hitbox):
        return self.interact_zone.colliderect(player_hitbox)

    def update(self, dt, chunk_grid, actual_map):
        super().update(actual_map)
