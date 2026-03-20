import pygame
from classes import entity
import math

# squelette fait par IA

class Boss(entity.Entity_That_Move_And_Has_Collision):
    def __init__(self, sprite, game_map, altitude_map=None, x=1500, y=1500, health=5000, damage=50, mob_spawned=None):
        super().__init__(sprite, game_map, altitude_map, x, y)

        # --- Stats du boss ---
        self.max_hp = health
        self.hp = self.max_hp
        self.damage = damage
        mob_spawned = mob_spawned if mob_spawned is not None else []
        self.speed = 1.2
        self.is_boss = True

        # --- IA ---
        self.target = None
        self.aggro_range = 400
        self.attack_range = 60
        self.attack_cooldown = 1200
        self.last_attack = pygame.time.get_ticks()

        # --- Apparence ---
        self.texture_index = 0
        self.animation_speed = 0.15

    def set_target(self, entity):
        """Définit la cible du boss (ex: joueur)."""
        self.target = entity

    def take_damage(self, amount):
        """Le boss prend des dégâts."""
        self.hp -= amount
        if self.hp <= 0:
            self.die()

    def die(self):
        """Mort du boss."""
        print("Boss defeated!")
        self.kill()

    def attack(self):
        """Attaque simple (à toi de définir les effets)."""
        now = pygame.time.get_ticks()
        if now - self.last_attack >= self.attack_cooldown:
            self.last_attack = now
            print("Boss attaque !")
            if self.target:
                # Ici tu peux appliquer des dégâts au joueur
                pass

    def update_ai(self):
        """IA basique : poursuite + attaque."""
        if not self.target:
            return

        # Distance à la cible
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        # Si trop loin → ignore
        if dist > self.aggro_range:
            return

        # Si à portée → attaque
        if dist < self.attack_range:
            self.attack()
            return

        # Sinon → poursuite
        if dist != 0:
            self.vx += (dx / dist) * self.speed
            self.vy += (dy / dist) * self.speed

    def update(self, chunk_grid, actual_map):
        """Update complet : IA + mouvement + collisions."""
        self.update_ai()

        # Animation
        self.texture_index += self.animation_speed
        self.texture_index %= len(self.sprite)
        self.image = self.sprite[int(self.texture_index)]

        # Update mouvement + collisions via parent
        super().update(chunk_grid, actual_map)
