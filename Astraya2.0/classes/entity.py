""" //c'est plus trop vrai//
pour créer un joueur de manière précise: 
player = Player(x=1500, y=1500)  # position initiale en pixels (1500, 1500) correspond à (93, 93) en tiles
player.x = 1600  # déplacer le joueur à x=1600 pixels (100 tiles)
player.y = 1400  # déplacer le joueur à y=1400 pixels (87   tiles)
player.get_pos()  # retourne (1600.0, 1400.0)
palyer.move(32, 0)  # déplacer le joueur de 32 pixels à droite (1 tile)
player.move(0, -32)  # déplacer le joueur de 32 pixels vers le haut (1 tile)
player.inventory.add_item(ITEMS["wood_sword"], quantity=1)  # ajouter une épée en bois à l'inventaire
player.selected_hotbar = 0  # sélectionner le premier slot de la hotbar (y'a pas encore de rendu de l'inventaire, mais c'est pour montrer comment ça marche)

les items du jeux ce touvent dans le items.py dans le dico ITEMS --> nv item --> "stick": Item("Bâton", item_type=ItemType.MISC, max_stack=64),
from items import get_item
epee = get_item("iron_sword")
player.inventory.add_item(epee)

"""



from turtle import pos

import pygame
import random
import engine
from inventory import Inventory
import settings

class Entity(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.direction = pygame.math.Vector2() # vecteur de direction (x, y) pour le mouvement
        self.animation_speed = 0.15
        self.speed = 0
        self.texture_index = 0
        
        

    #stats
    
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def get_pos(self):
        return (self.x, self.y)

    def update(self, dt):
        pass






