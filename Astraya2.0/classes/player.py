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
        self.anim_speed = 200-abs(self.vx)*15
        
        if self.life_point <= 0:
            self.dead = True
        if now - self.anim_timer >= self.anim_speed:
            if self.vx > 0.1:
                if self.texture_index < 3:
                    self.texture_index += 1
                else:
                    self.texture_index = 0
                self.anim_timer = now
            elif self.vx < -0.1:
                if self.texture_index < 4: self.texture_index = 4
                if self.texture_index < 7:
                    self.texture_index += 1
                else:
                    self.texture_index = 4
                self.anim_timer = now
            else:
                self.anim_frame = 0
            self.anim_timer = now
        if self.vx > 0.1:
            self.anim_speed = 200
            self.texture_index = 2 + self.anim_frame
        elif self.vx < -0.1:
            self.anim_speed = 200
            self.texture_index = 6 + self.anim_frame
        else:
            self.anim_speed = 400
            if self.last_orientation == "left":
                self.texture_index = 0 + self.anim_frame
            elif self.last_orientation == "right":
                self.texture_index = 4 + self.anim_frame

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
        self.move(dx * self.speed * dt, dy * self.speed * dt)
