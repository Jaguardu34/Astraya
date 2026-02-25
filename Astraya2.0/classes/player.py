import pygame
from .entity import Entity
from .inventory import Inventory
from engine import get_sprite
from settings import SCALE
from settings import *

class Player(Entity):
    def __init__(self, pos=(1500, 1500)):
        super().__init__(pos, groups=None)
        
        # inventory
        self.inventory = Inventory(size=20, hotbar_size=5)
        
        # load player sprite
        self.textures = pygame.image.load(pygame.image.load(settings.TEXTURES_PATH)).convert_alpha()
        
        self.texture_coeur = get_sprite(self.textures, 0, 241, 16, 16)
        texture_coeur_upscaled = pygame.transform.scale(self.texture_coeur, (self.texture_coeur.get_width()*SCALE, self.texture_coeur.get_height()*SCALE))
        self.rect = texture_coeur_upscaled.get_rect(topleft = pos)
        
        #hitbox plus petite que le sprite pour éviter les collisions trop précises qui bloquent le joueur
        self.hitbox = self.rect.inflate(HITBOX_OFFSET['player'],HITBOX_OFFSET['player']) #permet d'avoir une hitbox plus petite que le sprite pour éviter les collisions trop précises qui bloquent le joueur
        
        # stats
        self.stats = self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}
        
        

    def input(self): # le mouvement du joueur es généré dans la classe mère entity
        if not self.attacking:
            keys = pygame.key.get_pressed()

			# movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0


    def handle_event(self, event):
        # scroll molette → changer slot hotbar
        if event.type == pygame.MOUSEWHEEL:
            self.inventory.scroll_hotbar(-event.y)
        # clic gauche → utiliser item
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.inventory.use_selected(self)
        # touches 1-5 → sélectionner hotbar
        if event.type == pygame.KEYDOWN:
            for i, key in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]):
                if event.key == key:
                    self.inventory.select_hotbar(i)