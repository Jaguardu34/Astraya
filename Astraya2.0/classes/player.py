import math
import random

import math
import random

import pygame
import settings
import texture
from classes import entity, items
from classes.inventory import Inventory 



class Player(entity.Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=60):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.info_display = pygame.display.Info()
        self.WINDOW_SCALE = self.info_display.current_w, self.info_display.current_h
        self.x = float(x * 32)
        self.y = float(y * 32)
        self.speed = speed
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0
        sw = sprite[0].get_width() - 4
        sh = sprite[0].get_height() - 4
        self.hitbox = [pygame.Rect(self.x + 2, self.y + 2, sw, sh)]
        self.hitbox_size = sprite[0].get_width()
        self.show_on_minimap = True
        self.anim_timer = 0

        self.anim_speed = 0
        self.last_orientation = "left"
        self.has_life = True
        self.life_point = 20
        self.inventory = Inventory(size=20, hotbar_size=5)
        self.dead = False
       
        


    def update(self, chunk_grid, actual_map):
        super().update(chunk_grid, actual_map)
        now = pygame.time.get_ticks()

        if self.life_point <= 0:
            self.dead = True

        self.anim_speed = max(80, 200 - abs(self.vx) * 15)

        if self.vx > 0.1:
            self.last_orientation = "right"
            if now - self.anim_timer >= self.anim_speed:
                self.anim_timer = now
                self.texture_index = (self.texture_index % 3 + 1) % 3
        elif self.vx < -0.1:
            self.last_orientation = "left"
            if now - self.anim_timer >= self.anim_speed:
                self.anim_timer = now
                base = self.texture_index - 3 if self.texture_index >= 3 else 0
                self.texture_index = 3 + (base + 1) % 3
        elif self.vy > 0.1:
            self.last_orientation = "down"
            if now - self.anim_timer >= self.anim_speed:
                self.anim_timer = now
                base = self.texture_index - 6 if self.texture_index >= 3 else 0
                self.texture_index = 6 + (base + 1) % 3
        elif self.vy < -0.1:
            self.last_orientation = "down"
            if now - self.anim_timer >= self.anim_speed:
                self.anim_timer = now
                base = self.texture_index - 9 if self.texture_index >= 3 else 0
                self.texture_index = 9 + (base + 1) % 3
        
        else:
            if self.last_orientation == "right":
                self.texture_index = 0
            elif self.last_orientation == "left":
                self.texture_index = 3
            elif self.last_orientation == "down":
                self.texture_index = 6
            else : self.texture_index = 9

        def apply_deadzone(self, value, threshold=0.1):
            if abs(value) < threshold:
                return 0.0
            return value

    def input(self, keys, dt, joystick):
        dx, dy = 0, 0

        if joystick:
            joy_x = self.apply_deadzone(joystick.get_axis(0))
            joy_y = self.apply_deadzone(joystick.get_axis(1))
            dx = joy_x
            dy = joy_y

        if keys[settings.KEY_UP] or keys[pygame.K_UP]:
            dy = -1
        if keys[settings.KEY_DOWN] or keys[pygame.K_DOWN]:
            dy = 1
        if keys[settings.KEY_LEFT] or keys[pygame.K_LEFT]:
            dx = -1
        if keys[settings.KEY_RIGHT] or keys[pygame.K_RIGHT]:
            dx = 1

        if dx != 0 and dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

        if dx > 0.1:
            self.last_orientation = "right"
        elif dx < -0.1:
            self.last_orientation = "left"
        elif dy > 0.1:
            self.last_orientation = "down"
        elif dy < -0.1:
            self.last_orientation = "up"
        self.move(dx * self.speed * dt, dy * self.speed * dt)
