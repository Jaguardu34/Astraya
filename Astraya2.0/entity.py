import random
import pygame
import map

def check_collision_entites(ax, ay, bx, by, size=12):
    return abs(ax - bx) < size and abs(ay - by) < size

#verif collisions                   
def veriftile(x, y):
    if x < 0 or y < 0 or y >= len(map.map) or x >= len(map.map[y]) or x == None or y == None:
        return False
    elif map.map[y][x] in map.collide_tiles:
        return False
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
        if not veriftile(int(cx // 16), int(cy // 16)):
            return False

    return True


#class du poulet
class Animal:
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
                self.move((dist_x / dist) * self.speed * dt, (dist_y / dist) * self.speed * dt, now, chunk_grid)
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
class Player:
    def __init__(self, x=1500, y=1500, speed=100):
        self.x = float(x * 16)  # position en pixels monde
        self.y = float(y * 16)
        self.speed = speed # pixels par seconde
        self.vx = 0
        self.vy = 0
        
        
    def update(self):
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
            elif veriftile_pixel(collider.x + dx, collider.y):
                collider.vx += dx * 1.05

        if veriftile_pixel(self.x, new_y):
            collider = next((p for p in nearby if p is not self and check_collision_entites(self.x, new_y, p.x, p.y)), None)
            if collider is None:
                self.y = new_y
            elif veriftile_pixel(collider.x, collider.y + dy):
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