import pygame
import texture

MAX_HEARTS = 10  # 10 coeurs = 20 HP

class Coeurs():
    def __init__(self):
        self.surface = pygame.Surface((MAX_HEARTS * 42, 32), pygame.SRCALPHA)

    def draw(self, x, y, life, screen):
        self.surface.fill((0, 0, 0, 0))
        full = life // 2
        half = life % 2
        empty = MAX_HEARTS - full - half

        for i in range(full):
            self.surface.blit(texture.texture_coeur[0], (10 + (16 + 5) * i, 0))
        if half:
            self.surface.blit(texture.texture_coeur[1], (10 + (16 + 5) * full, 0))
        for i in range(empty):
            self.surface.blit(texture.texture_coeur[2], (10 + (16 + 5) * (full + half + i), 0))

        screen.blit(self.surface, (x, y))