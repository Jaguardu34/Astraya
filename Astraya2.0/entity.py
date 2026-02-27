import random
import pygame
from generate_map import *
from settings import SIZE, COLLIDE_TILES

def get_rect(x, y, size=12):
    return pygame.Rect(x - size//2, y - size//2, size, size)

def check_collision_entites(ax, ay, bx, by, size=16):
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
    """Vérifie si une tile est traversable (biome + altitude)."""
    if x < 0 or y < 0 or y >= SIZE or x >= SIZE:  # Utilise SIZE au lieu de len()
        return "ocean"
    
    biome_id = game_map[y, x]  #  Accès NumPy [y, x]
    
    # Vérification du biome (océan, montagnes, etc.)
    if biome_id in COLLIDE_TILES:
        return biome_id
    
    # verif altitude
    if altitude_map is not None:
        target_altitude = altitude_map[y, x]
        
        # Ne peut pas monter/descendre de plus d'1 niveau
        if abs(target_altitude - current_altitude) > 1:
            return "cliff"  # Blocké par une falaise
    
    return True  

def calculate_hitbox_size(sprite, shrink=2):
    surf = sprite[0]
    bounding = surf.get_bounding_rect()
    size = min(bounding.width, bounding.height) - shrink
    return max(4, size)

# ✅ MODIFICATION : Ajout de altitude_map et current_altitude
def veriftile_pixel(px, py, game_map, altitude_map=None, current_altitude=0, size=16):
    """Vérifie les 4 coins d'une hitbox."""
    half = size // 2
    center_x = px + half
    center_y = py + half
    corners = [
        (center_x - half + 1, center_y - half + 1),  # haut gauche
        (center_x + half - 1, center_y - half + 1),  # haut droite
        (center_x - half + 1, center_y + half - 1),  # bas gauche
        (center_x + half - 1, center_y + half - 1),  # bas droite
    ]
    for cx, cy in corners:
        result = veriftile(int(cx // 16), int(cy // 16), game_map, altitude_map, current_altitude)  # ✅ Passe altitude
        if result is not True:
            return result
    return True


class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500):  # ✅ Ajouter altitude_map
        super().__init__()
        self.x = float(x * 16)
        self.y = float(y * 16)
        self.sprite = sprite
        self.sprite_minimap = []
        self.texture_index = 0
        self.image = self.sprite[self.texture_index]
        self.rect = self.image.get_rect(topleft=(x * 16, y * 16))
        self.generate_minimap_sprite()
        self.game_map = game_map
        self.altitude_map = altitude_map  # ✅ NOUVEAU
        self.actual_map = game_map
        self.is_static = False
        self.hitbox_size = calculate_hitbox_size(sprite)
        
        # Initialiser l'altitude actuelle
        if altitude_map is not None:
            self.altitude = altitude_map[int(y), int(x)]
        else:
            self.altitude = 0

    def update_altitude(self):
        """Met à jour l'altitude selon la position actuelle."""  # ✅ NOUVEAU
        if self.altitude_map is not None:
            tile_x = int(self.x // 16)
            tile_y = int(self.y // 16)
            if 0 <= tile_x < SIZE and 0 <= tile_y < SIZE:
                self.altitude = self.altitude_map[tile_y, tile_x]

    def update(self, actual_map):
        self.texture_index = self.texture_index % len(self.sprite)
        self.actual_map = actual_map
        pass

    def generate_minimap_sprite(self):
        for i in range(len(self.sprite)):
            self.sprite_minimap.append(pygame.transform.scale(self.sprite[i], (self.sprite[i].get_width() // 2, self.sprite[i].get_height() // 2)))
    
    def draw(self, scalex, scaley, screen, scale, posx, posy):
        tile_cx = int(posx // 16)
        tile_cy = int(posy // 16)

        px = (self.x - (tile_cx - scalex//2) * 16) * scale
        py = (self.y - (tile_cy - scaley//2) * 16) * scale 

        if 0 <= px < scalex*16*scale and 0 <= py < scaley*16*scale:
            screen.blit(self.sprite[self.texture_index], (px, py))
    
    def draw_minimap(self, resolution_minimap, screen, scale, tile_cx, tile_cy):
        ptile_x = int(self.x // 16)
        ptile_y = int(self.y // 16)
        
        rel_x = ptile_x - tile_cx + scale // 2
        rel_y = ptile_y - tile_cy + scale // 2
        
        px = int(rel_x * resolution_minimap)
        py = int(rel_y * resolution_minimap)
        
        texture = self.sprite_minimap[self.texture_index]
        screen.blit(texture, (px, py))
    
    def get_pos(self):
        return (self.x, self.y)


class Entity_That_Move_And_Has_Collision(Entity):
    def update(self, chunk_grid, actual_map):
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            new_x = self.x + self.vx
            new_y = self.y + self.vy

            nearby = chunk_grid.get_nearby(new_x, new_y)
            rect_x = [pygame.Rect(new_x + 1, self.y + 1, self.hitbox_size//2, self.hitbox_size//2)]
            rect_y = [pygame.Rect(self.x + 1, new_y + 1, self.hitbox_size//2, self.hitbox_size//2)]

            #  Passer altitude_map et altitude actuelle
            if veriftile_pixel(new_x, self.y, self.actual_map, self.altitude_map, self.altitude) is True:
                blocked = False
                for p in nearby:
                    if p.game_map is not self.actual_map: continue
                    if p is self: continue
                    if p.is_static:
                        if p.has_hitbox and check_box_collide(p.hitbox, rect_x):
                            blocked = True
                            break
                    elif p.has_hitbox and check_box_collide(p.hitbox, rect_x):
                        if veriftile_pixel(p.x + self.vx, p.y, self.actual_map, self.altitude_map, self.altitude) is True:
                            p.vx += self.vx * 1.05
                        blocked = True
                        break
                if not blocked:
                    self.x = new_x

            # Passer altitude_map et altitude actuelle
            if veriftile_pixel(self.x, new_y, self.actual_map, self.altitude_map, self.altitude) is True:
                blocked = False
                for p in nearby:
                    if p.game_map is not self.actual_map: continue
                    if p is self: continue
                    if p.is_static:
                        if p.has_hitbox and check_box_collide(p.hitbox, rect_y):
                            blocked = True
                            break
                    elif p.has_hitbox and check_box_collide(p.hitbox, rect_y):
                        if veriftile_pixel(p.x, p.y + self.vy, self.actual_map, self.altitude_map, self.altitude) is True:
                            p.vy += self.vy * 1.05
                        blocked = True
                        break
                if not blocked:
                    self.y = new_y

            self.vx *= 0.8
            self.vy *= 0.8

        #  Mettre à jour l'altitude après chaque mouvement
        self.update_altitude()
        
        super().update(actual_map)

        
    def move(self, dx, dy):
        self.vx += dx
        self.vy += dy


class Animal(Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=2):  # ✅ Ajouter altitude_map
        super().__init__(sprite, game_map, altitude_map, x, y)  # ✅ Passer altitude_map
        self.last_animation = 0
        self.state = "walking"
        self.emoting_start = 0
        self.speed = speed
        self.cible_x = 0
        self.cible_y = 0
        self.last_walking_animation = 0
        self.anim_change_frame = random.randint(1000, 3000)
        self.emote_duration = random.randint(5000, 8000)
        self.blocked_move = 0
        self.vx = 0
        self.vy = 0
        self.random_cible()
        self.hitbox = [pygame.Rect(self.x, self.y, 16, 16)]
        self.has_hitbox = True

    def random_cible(self):
        self.cible_x = random.randint(int(self.x - 100), int(self.x + 100))
        self.cible_y = random.randint(int(self.y - 100), int(self.y + 100))

    def update(self, dt, chunk_grid, actual_map):
        now = pygame.time.get_ticks()

        if self.state == "walking":
            dist_x = self.cible_x - self.x
            dist_y = self.cible_y - self.y
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if dist > 1 and dist < 200:
                dx = (dist_x / dist) * self.speed * dt
                dy = (dist_y / dist) * self.speed * dt
                prev_x, prev_y = self.x, self.y
                self.move(dx, dy)
                self.check_blocked(dx, dy, prev_x, prev_y)
                self.animate_on_move(dx, dy, now)
            else:
                self.random_cible()
                self.anim_change_frame = random.randint(1000, 3000)
                self.emote_duration = random.randint(5000, 8000)
                self.state = "emoting"
                self.emoting_start = now

        elif self.state == "emoting":
            if now - self.emoting_start >= self.emote_duration:
                self.state = "walking"
            self.animate_action(now)

        super().update(chunk_grid, actual_map)
        self.hitbox[0].x = self.x
        self.hitbox[0].y = self.y

    def check_blocked(self, dx, dy, prev_x, prev_y):
        real_dist = ((self.x - prev_x)**2 + (self.y - prev_y)**2) ** 0.5
        expected_dist = (dx**2 + dy**2) ** 0.5

        if expected_dist > 0 and real_dist < expected_dist * 0.3:
            self.blocked_move += 1
        else:
            self.blocked_move = 0

        if self.blocked_move >= 20:
            self.cible_x = self.x + random.randint(-100, 100) - dx * 50
            self.cible_y = self.y + random.randint(-100, 100) - dy * 50
            self.blocked_move = 0

    def animate_action(self, now):
        pass

    def animate_on_move(self, dx, dy, now):
        pass

    
class Chicken(Animal):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):  # ✅ Ajouter altitude_map
        super().__init__(sprite, game_map, altitude_map, x, y)  # ✅ Passer altitude_map
        self.show_on_minimap = True
        
    def animate_action(self, now):
        if self.state != "emoting":
            return

        if now - self.last_animation >= self.anim_change_frame:
            if self.texture_index == 0:
                self.texture_index = 2
            else: 
                self.texture_index = 0 
            self.last_animation = now
    
    def animate_on_move(self, dx, dy, now):
        if now-self.last_walking_animation >= 500:
            if dx > 0:
                if self.texture_index != 1 :
                    self.texture_index = 1
                else: self.texture_index = 0
            elif dx < 0:
                if self.texture_index != 4:
                    self.texture_index = 4
                else: self.texture_index = 3
            self.last_walking_animation = now


class Player(Entity_That_Move_And_Has_Collision): 
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=40):  # ✅ Ajouter altitude_map
        super().__init__(sprite, game_map, altitude_map, x, y)  # ✅ Passer altitude_map
        self.x = float(x * 16)
        self.y = float(y * 16)
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.hitbox = [pygame.Rect(self.x, self.y, 16, 16)]
        self.show_on_minimap = True
        self.has_hitbox = True

    def update(self, chunk_grid, actual_map):
        super().update(chunk_grid, actual_map)
        self.hitbox[0].x = self.x
        self.hitbox[0].y = self.y

    def input(self, keys, dt):
        dx, dy = 0, 0
        if keys[pygame.K_z] or keys[pygame.K_UP]:    dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += 1
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:  dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1

        if dx != 0 and dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

        self.move(dx * self.speed * dt, dy * self.speed * dt)


class Object(Entity):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):  # ✅ Ajouter altitude_map
        super().__init__(sprite, game_map, altitude_map, x, y)  # ✅ Passer altitude_map
        self.is_static = True

    def update(self, dt, chunk_grid, actual_map):
        super().update(actual_map)
        
        
class Grotte(Object):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y)  
        self.hitbox = [
            pygame.Rect(self.x + 0,  self.y + 0,  48, 10),  # bord haut
            pygame.Rect(self.x + 0,  self.y + 0, 10, 20),   # bord gauche
            pygame.Rect(self.x + 38, self.y + 0, 10, 40)    # bord droit
        ]
        self.collide_action= [pygame.Rect(self.x + 5,  self.y + 5,  38, 20)]
        self.show_on_minimap = False
        self.has_hitbox = True

    def collides_with(self, player_rect):
        if self.game_map is self.actual_map:
            return check_box_collide(self.collide_action, player_rect)
        return False