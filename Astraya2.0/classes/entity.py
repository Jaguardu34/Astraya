"""
pour créer un joueur de manière précise: 
player = Player(x=1500, y=1500)  # position initiale en pixels (1500, 1500) correspond à (93, 93) en tiles
player.x = 1600  # déplacer le joueur à x=1600 pixels (100 tiles)
player.y = 1400  # déplacer le joueur à y=1400 pixels (87   tiles)
player.get_pos()  # retourne (1600.0, 1400.0)
palyer.move(32, 0)  # déplacer le joueur de 32 pixels à droite (1 tile)
player.move(0, -32)  # déplacer le joueur de 32 pixels vers le haut (1 tile)
player.inventory.add_item(ITEMS["wood_sword"], quantity=1)  # ajouter une épée en bois à l'inventaire
player.selected_hotbar = 0  # sélectionner le premier slot de la hotbar (y'a pas encore de rendu de l'inventaire, mais c'est pour montrer comment ça marche)
les items du jeux ce touvent dans le items.py dans le dico ITEMS
"""



import pygame
import random
import engine
from inventory import Inventory
class Entity:
    def __init__(self, x=1500, y=1500):
        self.x = float(x * 16)
        self.y = float(y * 16)
        self.speed = 0
        self.texture_index = 0

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if engine.veriftile_pixel(new_x, new_y):
            self._on_valid_move(new_x, new_y)

    def _on_valid_move(self, new_x, new_y):
        """À surcharger dans les sous-classes pour ajouter des conditions. c'est ##super()._on_valid_move(new_x, new_y)## pour faire le mouvement."""
        self.x = new_x
        self.y = new_y

    def get_pos(self):
        return (self.x, self.y)

    def update(self, dt):
        pass


class Chicken(Entity):
    def __init__(self, x=1500, y=1500):
        super().__init__(x, y)
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



class Player(Entity):
    def __init__(self, x=1500, y=1500):
        super().__init__(x, y)
        self.speed = 100
        self.hp = 100
        self.max_hp = 100
        self.inventory = Inventory(size=20, hotbar_size=5)

    def input(self, keys, dt):
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.move(0, -self.speed * dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(0, self.speed * dt)
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.move(-self.speed * dt, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(self.speed * dt, 0)

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