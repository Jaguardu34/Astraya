import pygame
import math
from classes import entity
import texture

class Ennemy(entity.Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, player, projectile_grp, altitude_map=None, x=1500, y=1500):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.player = player
        self.projectile_grp = projectile_grp
        self.last_shoot = pygame.time.get_ticks()
        self.firerate = 500
        self.show_on_minimap = True
        self.has_hitbox = True
        self.speed = 10

    def update(self, chunk_grid, actual_map, dt):
        super().update(chunk_grid, actual_map)
        dist_x = self.player.x - self.x
        dist_y = self.player.y - self.y
        dist = (dist_x**2 + dist_y**2) ** 0.5
        if dist < 500:
            dx = (dist_x / dist) * self.speed * dt
            dy = (dist_y / dist) * self.speed * dt
            now = pygame.time.get_ticks()
            if now - self.last_shoot >= self.firerate:
                self.last_shoot = now
                self.shoot()
            self.move(dx, dy)

    def shoot(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        angle = math.degrees(math.atan2(dy, dx))
        p = entity.Projectile(texture.texture_chicken, self.actual_map, self, int(angle), 30, None, self.x, self.y)
        self.projectile_grp.add(p)