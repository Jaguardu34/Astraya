import random
import pygame
from settings import *
from classes.npc import Npc
from texture import *
import numpy as np
import math
 
#========================================
# Classes pour la génération de villages
# Une village et une Building
#========================================
 
 
class Village:
    def __init__(self, x, y, village_type, biome):
        self.x = x  
        self.y = y
        self.type = village_type  
        self.biome = biome
        self.buildings = []  
        self.roads = []  
        self.decorations = []  
        self.radius = VILLAGE_TYPES[village_type]["radius"]
        
    def generate(self, biome_map=None):
        """Génère le plan complet du village."""
        config = VILLAGE_TYPES[self.type]
        
        # Générer le centre (puits)
        self.generate_center()
        
        # Générer les bâtiments principaux
        for building_type, min_count, max_count in config["buildings"]:
            count = random.randint(min_count, max_count)
            for _ in range(count):
                self.add_building(building_type, biome_map)
 
    def generate_center(self):
        """Génère le centre du village avec un puits."""
        # Tous les villages ont un puits au centre
        self.add_building_at("puteus", self.x, self.y)
 
    def add_building(self, building_type, biome_map=None):
        """Ajoute un bâtiment à une position libre."""
        attempts = 0
        while attempts < 100:
            # Position aléatoire dans le rayon du village
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(5, self.radius / 2)
            
            bx = int(self.x + distance * np.cos(angle))
            by = int(self.y + distance * np.sin(angle))
            
            # Vérifier si la position est valide
            if self.can_place_building(bx, by, building_type, biome_map):
                building = Building(bx, by, building_type)
                self.buildings.append(building)
                return True
            
            attempts += 1
        
        return False
    
    def add_building_at(self, building_type, x, y):
        """Place un bâtiment à une position précise."""
        building = Building(x, y, building_type)
        self.buildings.append(building)
 
 
    def can_place_building(self, x, y, building_type, biome_map=None):
        """Vérifie si on peut placer un bâtiment ici."""
        size = BUILDING_TYPES[building_type]["size"]
        
        # Vérifier limites de la map
        if x < 10 or y < 10 or x > SIZE - 10 or y > SIZE - 10:
            return False
        
        # Vérifier que le biome n'est pas interdit (eau ou sable)
        if biome_map is not None:
            # Vérifier plusieurs points du bâtiment
            for dx in range(size[0]):
                for dy in range(size[1]):
                    check_x = min(x + dx, SIZE - 1)
                    check_y = min(y + dy, SIZE - 1)
                    tile_biome = biome_map[check_y, check_x]
                    
                    if tile_biome in FORBIDDEN_VILLAGE_BIOMES:
                        return False
        else:
            # Fallback si pas de biome_map (vérifier le biome du village)
            if self.biome in FORBIDDEN_VILLAGE_BIOMES:
                return False
        
        # Vérifier collision avec autres bâtiments
        for building in self.buildings:
            if self.buildings_overlap(x, y, size, building):
                return False
        
        return True
    
    def buildings_overlap(self, x, y, size, other_building):
        """Vérifie si deux bâtiments se chevauchent."""
        other_size = BUILDING_TYPES[other_building.type]["size"]
        
        # Rectangle du nouveau bâtiment
        r1 = pygame.Rect(x, y, size[0], size[1])
        # Rectangle du bâtiment existant
        r2 = pygame.Rect(other_building.x, other_building.y, 
                        other_size[0], other_size[1])
        
        # Ajouter une marge de sécurité (2 tiles)
        r1.inflate_ip(4, 4)
        r2.inflate_ip(4, 4)
        
        return r1.colliderect(r2)
 
 
    def generate_decorations(self):
        """Ajoute statues, amphores, jardins, etc."""
        num_decorations = len(self.buildings) * 2
        
        for _ in range(num_decorations):
            # Choisir un type de décoration selon le type de village
            if self.type == "city":
                deco_type = random.choice([
                    "statue", "fountain", "column", "garden", "amphora"
                ])
            else:  # hamlet
                deco_type = random.choice([
                    "amphora", "animal", "garden"
                ])
            
            # Position aléatoire
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(5, self.radius)
            dx = int(self.x + distance * np.cos(angle))
            dy = int(self.y + distance * np.sin(angle))
            
            self.decorations.append({
                "type": deco_type,
                "x": dx,
                "y": dy
            })
 
 
class Building:
    def __init__(self, x, y, building_type):
        self.x = x
        self.y = y
        self.type = building_type
        self.size = BUILDING_TYPES[building_type]["size"]
        self.rotation = random.choice([0, 90, 180, 270])  # Orientation
 

def spawn_villageois(village, game_map):
    villagers = []
    num_villagers = len(village.buildings) // 2
    
    for _ in range(num_villagers):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(5, village.radius)
        vx = int(village.x + distance * math.cos(angle))
        vy = int(village.y + distance * math.sin(angle))

        npc_type = "fermier"
        texture = texture_chicken_corrupted  

        villagers.append(
            Npc(
                npc_type,
                texture,
                game_map,
                ["Salut ! Je suis un fermier.", "Bonne journée !"],
                altitude_map=None,
                x=vx,
                y=vy
            )
        )

    return villagers