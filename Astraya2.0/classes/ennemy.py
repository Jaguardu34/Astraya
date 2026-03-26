import pygame
import math
from classes import entity
import texture
import random

class Corrupted_Chicken(entity.Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, player, projectile_grp, altitude_map=None, x=1500, y=1500):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.player = player
        self.projectile_grp = projectile_grp
        self.last_shoot = pygame.time.get_ticks()
        self.firerate_base = 3000
        self.firerate = self.firerate_base
        self.show_on_minimap = True
        self.has_hitbox = True
        self.speed = 10
        self.state = "walking"
        self.last_walking_animation = 0
        self.last_shoot_anim = 0
        self.texture_index = 0
        self.trigger_distance = 1000
        self.last_direction = "right"

    def update(self, chunk_grid, actual_map, dt):
        super().update(chunk_grid, actual_map)

        dist_x = float(self.player.x - self.x)
        dist_y = float(self.player.y - self.y)

        dist = float((dist_x**2 + dist_y**2) ** 0.5)
        if dist < self.trigger_distance:
            dx = ((dist_x / dist) * self.speed * dt)
            dy = ((dist_y / dist) * self.speed * dt)
            now = pygame.time.get_ticks()
            self.update_texture(dx, dy, now)
            if now - self.last_shoot >= self.firerate:
                self.firerate = random.randint(self.firerate_base-500, self.firerate_base+500)
                self.state = "shooting"
                self.last_shoot = now
                self.move(0, 0)
                self.shoot()
            
            if now-self.last_shoot >= 1000:
                self.move(dx, dy)
                self.state = "walking"
        else:
            self.state = "static"
            

    def shoot(self):
        self.stat = self.shoot
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        angle = math.degrees(math.atan2(dy, dx))
        p = entity.Projectile(texture.texture_oeuf, self.actual_map, self, int(angle), 30, None, self.x, self.y)
        self.projectile_grp.add(p)
    
    def update_texture(self, dx, dy, now):
        if self.state == "static":
            if self.last_direction == "right":
                self.texture_index = 0
            elif self.last_direction == "left":
                self.texture_index = 3
        elif self.state == "walking":
            if now - self.last_walking_animation >= 500:
                if dx > 0:
                    self.last_direction = "right"
                    if self.texture_index != 1:
                        self.texture_index = 1
                    else:
                        self.texture_index = 0
                elif dx < 0:
                    self.last_direction = "left"
                    if self.texture_index != 4:
                        self.texture_index = 4
                    else:
                        self.texture_index = 3
                self.last_walking_animation = now
        elif self.state == "shooting":
            if self.last_direction == "right":
                self.texture_index = 2
            elif self.last_direction == "left":
                self.texture_index = 5
            