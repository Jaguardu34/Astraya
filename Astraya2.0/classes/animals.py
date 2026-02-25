import pygame
from .entity import Entity
import engine

#à modifier

class Chicken(Entity):
    def __init__(self, pos=(1500, 1500)):
        super().__init__(pos, groups=None)
        self.speed = 10
        self.last_animation = 0
        self.emoting_state = False
        self.emoting_start = 0
        self.last_emoting = 0
        self.emoting_duration = 0
        self.last_walking_animation = 0
        self.cible_x = 0
        self.cible_y = 0
        self.random_cible()

    def random_cible(self):
        self.cible_x = random.randint(int(self.x - 50), int(self.x + 50))
        self.cible_y = random.randint(int(self.y - 50), int(self.y + 50))

    def _on_valid_move(self, new_x, new_y):
        if not any(engine.check_collision_entites(new_x, new_y, p.x, p.y) for p in engine.tab_poulet if p is not self):
            if not engine.check_collision_entites(new_x, new_y, engine.player.x, engine.player.y):
                self.x = new_x
                self.y = new_y

    def update(self, dt):
        self.animate()
        now = pygame.time.get_ticks()

        if self.emoting_state:
            if now - self.last_emoting >= self.emoting_duration:
                self.emoting_state = False
        else:
            dist_x = self.cible_x - self.x
            dist_y = self.cible_y - self.y
            dist = (dist_x ** 2 + dist_y ** 2) ** 0.5

            if dist > 1:
                self._walk(dist_x, dist_y, dist, dt)
            else:
                self.random_cible()
                self.emoting_state = True
                self.emoting_start = now
                self.last_emoting = now
                self.emoting_duration = random.randint(5000, 8000)

    def _walk(self, dist_x, dist_y, dist, dt):
        now = pygame.time.get_ticks()
        dx = (dist_x / dist) * self.speed * dt
        dy = (dist_y / dist) * self.speed * dt
        self.move(dx, dy)

        if now - self.last_walking_animation >= 500:
            if dx > 0:
                self.texture_index = 1 if self.texture_index == 0 else 0
            elif dx < 0:
                self.texture_index = 7 if self.texture_index == 6 else 6
            self.last_walking_animation = now

    def animate(self):
        now = pygame.time.get_ticks()
        if self.emoting_state:
            if now - self.last_animation >= self.emoting_duration // 2:
                self.texture_index = 3 if self.texture_index == 0 else 0
                self.last_animation = now