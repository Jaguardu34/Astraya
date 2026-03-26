import pygame
from classes import entity
import random

class Grotte(entity.Object):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.hitbox = [
            pygame.Rect(self.x + 0,  self.y + 0,  48, 10),
            pygame.Rect(self.x + 0,  self.y + 0,  10, 20),
            pygame.Rect(self.x + 38, self.y + 0,  10, 40)
        ]
        self.collide_action = [pygame.Rect(self.x + 5, self.y + 5, 38, 20)]
        self.show_on_minimap = False
        self.has_hitbox = True
        self.has_life = False

    def collides_with(self, player_rect):
        if self.game_map is self.actual_map:
            return entity.check_box_collide(self.collide_action, player_rect)
        return False


class Block(entity.Object):
    def __init__(self, sprite, game_map, item, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.item = item
        self.hitbox = [pygame.Rect(self.x, self.y, 32, 32)]
        self.show_on_minimap = False
        self.has_hitbox = True
        self.has_life = False

class Plant(entity.Object):
    def __init__(self, sprite, game_map, nbr_texture, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y, speed)
        self.has_hitbox = False
        self.has_life = False
        self.texture_index = random.randint(0, nbr_texture)

class Tree(entity.Object):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, speed=10):
        super().__init__(sprite, game_map, altitude_map, x, y, speed)
        self.has_hitbox = True
        self.has_life = True          # ← était False
        self.life_point = 5           # ← 5 coups de hache
        self.max_life_point = 5
        self.hitbox = [pygame.Rect(self.x+10, self.y+30, 44, 20)]
