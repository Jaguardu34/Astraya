import pygame
from classes import entity, ennemy
import math
import random
import texture

class Boss(entity.Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, health=5000, damage=50, mob_spawned=None):
        super().__init__(sprite, game_map, altitude_map, x, y)

        # --- Stats ---
        self.max_hp = health
        self.hp = self.max_hp
        self.damage = damage
        self.speed = 0.2
        self.is_boss = True

        # --- IA ---
        self.target = None
        self.aggro_range = 400
        self.attack_range = 60
        self.attack_cooldown = 1200
        self.last_attack = pygame.time.get_ticks()

        # --- Spawn mobs ---
        self.spawn_cooldown = 5000
        self.last_spawn = pygame.time.get_ticks()
        
        # --- Apparence ---
        self.texture_index = 0
        self.animation_speed = 0.15
        self.show_on_minimap = True

    # --------------------------
    #   ACTIONS DU BOSS
    # --------------------------

    def attack(self):
        """Attaque le joueur si assez proche."""
        now = pygame.time.get_ticks()
        if now - self.last_attack < self.attack_cooldown:
            return

        self.last_attack = now
        print("Boss attaque !")

        if self.target:
            # Vérifie collision simple
            dist = math.hypot(self.target.x - self.x, self.target.y - self.y)
            if dist < self.attack_range:
                if hasattr(self.target, "life_point"):
                    self.target.life_point -= self.damage
                    print("Le joueur prend", self.damage, "dégâts")

    def spawn_minion(self):
        """Fait apparaître un poulet corrompu autour du boss."""
        now = pygame.time.get_ticks()
        if now - self.last_spawn < self.spawn_cooldown:
            return

        self.last_spawn = now
        print("Boss invoque un poulet corrompu !")

        # Position aléatoire autour du boss
        angle = random.random() * math.tau
        dist = 80
        sx = int((self.x + math.cos(angle) * dist) // 32)
        sy = int((self.y + math.sin(angle) * dist) // 32)

        # Spawn
        chicken = ennemy.Corrupted_Chicken(
            texture.texture_chicken_corrupted,
            self.actual_map,
            self.target,
            self.projectile_grp, 
            self.altitude_map,
            sx, sy
        )

        # Ajout dans le groupe d'entités
        # Le boss n'a pas accès direct aux groupes → on utilise un hack :
        if hasattr(self, "groups"):
            for g in self.groups():
                g.add(chicken)

    # --------------------------
    #   IA PRINCIPALE
    # --------------------------

    def set_target(self, entity):
        self.target = entity


    def update_ai(self):
        if not self.target:
            return

        # Distance
        dx = float(self.target.x - self.x)
        dy = float(self.target.y - self.y)

        dist = math.sqrt(dx*dx + dy*dy)

        if dist > self.aggro_range:
            return

        # Attaque
        if dist < self.attack_range:
            self.attack()
        else:
            # Poursuite
            if dist != 0:
                self.vx += (dx / dist) * self.speed
                self.vy += (dy / dist) * self.speed

        # Spawn de mobs
        self.spawn_minion()

    # --------------------------
    #   UPDATE GLOBAL
    # --------------------------

    def update(self, dt, chunk_grid, actual_map):
        self.update_ai()

        # Animation
        self.texture_index += self.animation_speed
        self.texture_index %= len(self.sprite)
        frame = int(self.texture_index)
        self.image = self.sprite[frame]

        # Mouvement + collisions
        super().update(chunk_grid, actual_map)
