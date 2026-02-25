import random
import pygame
import map

def get_rect(x, y, size=12):
    return pygame.Rect(x - size//2, y - size//2, size, size)

def check_collision_entites(ax, ay, bx, by, size=12):
    return get_rect(ax, ay, size).colliderect(get_rect(bx, by, size))

#verif collisions                   
def veriftile(x, y):
    if x < 0 or y < 0 or y >= len(map.map) or x >= len(map.map[y]) or x == None or y == None:
        return "ocean"
    elif map.map[y][x] in map.collide_tiles:
        return map.map[y][x]
    else:
        return True

def veriftile_pixel(px, py, size=12):
    cx_center = px + 8  
    cy_center = py + 8
    half = size // 2
    corners = [
        (cx_center - half, cy_center - half),  # haut gauche
        (cx_center + half, cy_center - half),  # haut droite
        (cx_center - half, cy_center + half),  # bas gauche
        (cx_center + half, cy_center + half),  # bas droite
    ]
    for cx, cy in corners:
        result = veriftile(int(cx // 16), int(cy // 16))
        if result is not True:
            return result

    return True


#class du poulet
class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite, x=1500, y=1500):
        super().__init__()
        self.x = float(x * 16)
        self.y = float(y * 16)
        self.sprite = sprite
        self.sprite_minimap = []
        self.texture_index = 0
        self.image = self.sprite[self.texture_index]
        self.rect = self.image.get_rect(topleft=(x * 16, y * 16))
        self.generate_minimap_sprite()


    def update(self):
        self.image = self.sprite[self.texture_index]
        pass

    def generate_minimap_sprite(self):
        for i in range(len(self.sprite)):
            self.sprite_minimap.append(pygame.transform.scale(self.sprite[i], (self.sprite[i].get_width() // 2, self.sprite[i].get_height() // 2)))
            
    
    def draw(self, x, y, scalex, scaley, screen, scale, posx, posy):
        tile_cx = int(posx // 16)
        tile_cy = int(posy // 16)

        offset_x = int(posx % 16) * scale
        offset_y = int(posy % 16) * scale
        px = x + (self.x - (tile_cx - scalex//2) * 16) * scale - offset_x
        py = y + (self.y - (tile_cy - scaley//2) * 16) * scale - offset_y

        if 0 <= px < scalex*16*scale and 0 <= py < scaley*16*scale:
            screen.blit(self.sprite[self.texture_index], (px, py))
    
    def draw_minimap(self, x, y, resolution_minimap, screen, scale, tile_cx, tile_cy, map_decouverte):
        # position du poulet en tiles
        ptile_x = int(self.x // 16)
        ptile_y = int(self.y // 16)
        
        rel_x = ptile_x - tile_cx + scale // 2
        rel_y = ptile_y - tile_cy + scale // 2
        
        px = x + int(rel_x * resolution_minimap)
        py = y + int(rel_y * resolution_minimap)
        
        if (ptile_x, ptile_y) in map_decouverte:
            if x <= px < x + scale * resolution_minimap and y <= py < y + scale * resolution_minimap:
                texture = self.sprite_minimap[self.texture_index]
                screen.blit(texture, (px-8, py-8))
            

class Animal(Entity):
    def __init__(self, sprite, x, y, speed=10):
        super().__init__(sprite, x, y)
        self.last_animation = 0
        self.state = "walking"
        self.emoting_start = 0
        self.speed = speed
        self.cible_x = 0
        self.cible_y = 0
        self.last_walking_animation = 0
        self.anim_change_frame = random.randint(1000, 3000)
        self.emote_duration = random.randint(5000, 8000)
        self.blocked_move= 0
        self.vx = 0
        self.vy = 0
        self.random_cible()

    def random_cible(self):
        self.cible_x = random.randint(int(self.x-100), int(self.x+100))
        self.cible_y = random.randint(int(self.y-100), int(self.y+100))

    def update(self, dt, chunk_grid, player_x=0, player_y=0):
        super().update()
        now = pygame.time.get_ticks()
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            if veriftile_pixel(self.x + self.vx, self.y):
                self.x += self.vx
            if veriftile_pixel(self.x, self.y + self.vy):
                self.y += self.vy
            self.vx *= 0.8  # friction
            self.vy *= 0.8
        self.animate_action(now)
        if self.state == "emoting":
            if now - self.emoting_start >= self.emote_duration:
                self.state = "walking"
                self.last_animation = now
        elif self.state == "walking":
            dist_x = self.cible_x - self.x
            dist_y = self.cible_y - self.y
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if dist > 1:
                if dist < 200:
                    self.move((dist_x / dist) * self.speed * dt, (dist_y / dist) * self.speed * dt, now, chunk_grid)
                else: self.random_cible()
            else:
                self.random_cible()
                self.anim_change_frame = random.randint(1000, 3000)
                self.emote_duration = random.randint(5000, 8000)
                self.state = "emoting"
                self.emoting_start = now
                    
    def move(self, dx, dy, now, chunk_grid):
        new_x = self.x + dx
        new_y = self.y + dy
        nearby = chunk_grid.get_nearby(new_x, new_y)
        prev_x, prev_y = self.x, self.y

        if veriftile_pixel(new_x, self.y):
            collider = self.can_move(new_x, self.y, nearby)
            if collider is None:
                self.x = new_x
            elif not isinstance(collider, Object):
                if veriftile_pixel(collider.x + dx, collider.y):
                    collider.vx += dx * 1.05
                    self.x = new_x

        if veriftile_pixel(self.x, new_y):
            collider = self.can_move(self.x, new_y, nearby)
            if collider is None:
                self.y = new_y
            elif not isinstance(collider, Object):    
                if veriftile_pixel(collider.x, collider.y + dy):
                    collider.vy += dy * 1.05
                    self.y = new_y

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

        if self.x != prev_x or self.y != prev_y:
            self.animate_on_move(dx, dy, now)
   
                
    def animate_action(self, now):
        pass
        
    def animate_on_move(self, dx, dy, now):
        pass

    def can_move(self, x, y, nearby):
        collider = next((p for p in nearby if p is not self and check_collision_entites(x, y, p.x, p.y)), None)
        return collider            
    
class Chicken(Animal):
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




#class du joueur
class Player(Entity):
    def __init__(self, sprite, x=1500, y=1500, speed=100):
        super().__init__(sprite, x, y)
        self.x = float(x * 16)  # position en pixels monde
        self.y = float(y * 16)
        self.speed = speed # pixels par seconde
        self.vx = 0
        self.vy = 0
        
        
    def update(self):
        super().update()
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            if veriftile_pixel(self.x + self.vx, self.y):
                self.x += self.vx
            if veriftile_pixel(self.x, self.y + self.vy):
                self.y += self.vy
            self.vx *= 0.8  # friction
            self.vy *= 0.8
        
    def move(self, dx, dy, chunk_grid):
        new_x = self.x + dx
        new_y = self.y + dy
        nearby = chunk_grid.get_nearby(new_x, new_y)
        if veriftile_pixel(new_x, self.y):
            collider = next((p for p in nearby if p is not self and check_collision_entites(new_x, self.y, p.x, p.y)), None)
            if collider is None:
                self.x = new_x
            elif not isinstance(collider, Object):
                if veriftile_pixel(collider.x + dx, collider.y):
                    collider.vx += dx * 1.05

        if veriftile_pixel(self.x, new_y):
            collider = next((p for p in nearby if p is not self and check_collision_entites(self.x, new_y, p.x, p.y)), None)
            if collider is None:
                self.y = new_y
            elif not isinstance(collider, Object):
                if veriftile_pixel(collider.x, collider.y + dy):
                    collider.vy += dy * 1.05

    def input(self, keys, dt, chunk_grid):
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.move(0, -self.speed * dt, chunk_grid)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(0, self.speed * dt, chunk_grid)
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.move(-self.speed * dt, 0, chunk_grid)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(self.speed * dt, 0, chunk_grid)

    def get_pos(self):
        return (self.x, self.y)  # en pixels
    
    
class Ennemy():
    def __init__(self, x=1500, y=1500, speed=10):
        self.x = float(x * 16)
        self.y = float(y * 16)
        self.texture_index = 0
        self.last_animation = 0
        self.state = "walking"
        self.emoting_start = 0
        self.speed = speed
        self.cible_x = 0
        self.cible_y = 0
        self.last_walking_animation = 0
        self.anim_change_frame = random.randint(1000, 3000)
        self.emote_duration = random.randint(5000, 8000)
        self.blocked_move= 0
        self.vx = 0
        self.vy = 0
        self.random_cible()



    def random_cible(self):
        self.cible_x = random.randint(int(self.x-100), int(self.x+100))
        self.cible_y = random.randint(int(self.y-100), int(self.y+100))

    def update(self, dt, chunk_grid):
        now = pygame.time.get_ticks()
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            if veriftile_pixel(self.x + self.vx, self.y):
                self.x += self.vx
            if veriftile_pixel(self.x, self.y + self.vy):
                self.y += self.vy
            self.vx *= 0.8  # friction
            self.vy *= 0.8
        now = pygame.time.get_ticks()
        self.animate_action(now)
        if self.state == "emoting":
            if now - self.emoting_start >= self.emote_duration:
                self.state = "walking"
                self.last_animation = now
        elif self.state == "walking":
            dist_x = self.cible_x - self.x
            dist_y = self.cible_y - self.y
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if dist > 1:
                if dist < 200:
                    self.move((dist_x / dist) * self.speed * dt, (dist_y / dist) * self.speed * dt, now, chunk_grid)
                else: self.random_cible()
            else:
                self.random_cible()
                self.anim_change_frame = random.randint(1000, 3000)
                self.emote_duration = random.randint(5000, 8000)
                self.state = "emoting"
                self.emoting_start = now
                    
    def move(self, dx, dy, now, chunk_grid):
        new_x = self.x + dx
        new_y = self.y + dy
        nearby = chunk_grid.get_nearby(new_x, new_y)
        prev_x, prev_y = self.x, self.y

        if veriftile_pixel(new_x, self.y):
            collider = self.can_move(new_x, self.y, nearby)
            if collider is None:
                self.x = new_x
            elif veriftile_pixel(collider.x + dx, collider.y):
                collider.vx += dx * 1.05
                self.x = new_x

        if veriftile_pixel(self.x, new_y):
            collider = self.can_move(self.x, new_y, nearby)
            if collider is None:
                self.y = new_y
            elif veriftile_pixel(collider.x, collider.y + dy):
                collider.vy += dy * 1.05
                self.y = new_y

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

        if self.x != prev_x or self.y != prev_y:
            self.animate_on_move(dx, dy, now)
   
                
    def animate_action(self, now):
        pass
        
    def animate_on_move(self, dx, dy, now):
        pass

    def can_move(self, x, y, nearby):
        collider = next((p for p in nearby if p is not self and check_collision_entites(x, y, p.x, p.y)), None)
        return collider
    

class Object(Entity):
    def update(self, dt, chunk_grid, player_x=0, player_y=0):
        super().update()
        if check_collision_entites(self.x, self.y, player_x, player_y, size=24):
            self.collision()

    def check_collision(self, player_x, player_y):
        if check_collision_entites(self.x, self.y, player_x, player_y, size=24):
            return True
        
    def collision(self):
        pass
        
class Grotte(Object):
    
    def collision(self):
        pass
    