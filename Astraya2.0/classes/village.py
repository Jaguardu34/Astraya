import random
import pygame
from generate_map import *
from settings import *

#========================================
# Classes pour la génération de villages
# Une village et une Building
#========================================


class Village:
    def __init__(self, x, y, village_type, biome):
        self.x = x  # Position centrale
        self.y = y
        self.type = village_type  # "hamlet", "village", "city"
        self.biome = biome
        self.buildings = []  # Liste de Building
        self.roads = []  # Liste de segments de route
        self.decorations = []  # Amphores, statues, etc.
        self.radius = VILLAGE_TYPES[village_type]["radius"]
        
    def generate(self):
        """Génère le plan complet du village."""
        config = VILLAGE_TYPES[self.type]
        
        # Générer le centre (puits, forum, etc.)
        self.generate_center()
        
        # Générer les bâtiments principaux
        for building_type, min_count, max_count in config["buildings"]:
            count = random.randint(min_count, max_count)
            for _ in range(count):
                self.add_building(building_type)

    def generate_center(self):
        """Génère le centre du village avec des éléments décoratifs."""

        if self.type == "hamlet":
            # Hameau : puits au centre
            self.add_building_at("puteus", self.x, self.y)
        elif self.type == "village":
            # Village : temple ou place
            self.add_building_at("sacellum", self.x, self.y)
        else:
            # Ville : forum
            self.add_building_at("forum", self.x, self.y)

    def add_building(self, building_type):
        """Ajoute un bâtiment à une position libre."""
        attempts = 0
        while attempts < 100:
            # Position aléatoire dans le rayon du village
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(5, self.radius)
            
            bx = int(self.x + distance * np.cos(angle))
            by = int(self.y + distance * np.sin(angle))
            
            # Vérifier si la position est valide
            if self.can_place_building(bx, by, building_type):
                building = Building(bx, by, building_type)
                self.buildings.append(building)
                return True
            
            attempts += 1
        
        return False
    
    def add_building_at(self, building_type, x, y):
        """Place un bâtiment à une position précise."""
        building = Building(x, y, building_type)
        self.buildings.append(building)


    def can_place_building(self, x, y, building_type):
        """Vérifie si on peut placer un bâtiment ici."""
        size = BUILDING_TYPES[building_type]["size"]
        
        # Vérifier limites de la map
        if x < 10 or y < 10 or x > SIZE - 10 or y > SIZE - 10:
            return False
        
        # Vérifier biome (pas dans l'océan)
        if map[y, x] == BIOME_IDS["ocean"]:
            return False
        
        # Vérifier collision avec autres bâtiments
        for building in self.buildings:
            if self.buildings_overlap(x, y, size, building):
                return False
        
        return True


    def generate_decorations(self):
        """Ajoute statues, amphores, jardins, etc."""
        num_decorations = len(self.buildings) * 2
        
        for _ in range(num_decorations):
            # Choisir un type de décoration selon le type de village
            if self.type == "city":
                deco_type = random.choice([
                    "statue", "fountain", "column", "garden", "amphora"
                ])
            elif self.type == "village":
                deco_type = random.choice([
                    "cart", "amphora", "animal", "garden"
                ])
            else:
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