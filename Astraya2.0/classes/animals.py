import random
from classes import entity
import pygame

class Animal(entity.Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y)
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
        self.random_cible()
        self.has_life = True
        self.life_point = 3

    def random_cible(self):
        for _ in range(20):
            cx = random.randint(int(self.x - 100), int(self.x + 100))
            cy = random.randint(int(self.y - 100), int(self.y + 100))
            tile_x = int(cx // 32)
            tile_y = int(cy // 32)
            if entity.veriftile(tile_x, tile_y, self.actual_map, self.altitude_map, self.altitude) is True:
                self.cible_x = cx
                self.cible_y = cy
                return
        self.cible_x = self.x
        self.cible_y = self.y

    def update(self, dt, chunk_grid, actual_map):
        now = pygame.time.get_ticks()

        if self.state == "walking":
            dist_x = self.cible_x - self.x
            dist_y = self.cible_y - self.y
            dist = (dist_x**2 + dist_y**2) ** 0.5

            if dist > 200:
                self.random_cible()

            if dist > 1:
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

        if self.life_point <= 0:
            self.kill()
            return

    def check_blocked(self, dx, dy, prev_x, prev_y):
        real_dist = ((self.x - prev_x)**2 + (self.y - prev_y)**2) ** 0.5
        expected_dist = (dx**2 + dy**2) ** 0.5
        if expected_dist < 0.1:
            return
        if real_dist < expected_dist * 0.3:
            self.blocked_move += 1
        else:
            self.blocked_move = 0
        if self.blocked_move >= 20:
            self.cible_x = self.x + random.randint(-100, 100)
            self.cible_y = self.y + random.randint(-100, 100)
            self.blocked_move = 0

    def animate_action(self, now):
        pass

    def animate_on_move(self, dx, dy, now):
        pass


class Chicken(Animal):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=4):
        super().__init__(sprite, game_map, altitude_map, x, y, speed)
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
        if now - self.last_walking_animation >= 500:
            if dx > 0:
                if self.texture_index != 1:
                    self.texture_index = 1
                else:
                    self.texture_index = 0
            elif dx < 0:
                if self.texture_index != 4:
                    self.texture_index = 4
                else:
                    self.texture_index = 3
            self.last_walking_animation = now