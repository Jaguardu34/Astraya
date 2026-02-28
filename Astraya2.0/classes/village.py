import random
import pygame
from generate_map import *
from settings import *
import numpy as np

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
        if self.biome == BIOME_IDS["ocean"]:
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


def draw_village(village, screen, camera_pos, offset_x, offset_y, scale):
    """Dessine un village complet."""
    tile_cx = int(camera_pos[0] // 16)
    tile_cy = int(camera_pos[1] // 16)
    scalex = scale[0]
    scaley = scale[1]

    for building in village.buildings:
        bx = (building.x - (tile_cx - scalex//2)) * 16 * scale - offset_x
        by = (building.y - (tile_cy - scaley//2)) * 16 * scale - offset_y
        
        # Vérifier si visible
        if -50 <= bx < (scalex+1)*16*scale and -50 <= by < (scaley+1)*16*scale:
            draw_building(building, screen, bx, by, scale)
    
    # 3. Dessiner les décorations
    for deco in village.decorations:
        dx = (deco["x"] - (tile_cx - scalex//2)) * 16 * scale - offset_x
        dy = (deco["y"] - (tile_cy - scaley//2)) * 16 * scale - offset_y
        
        if -50 <= dx < (scalex+1)*16*scale and -50 <= dy < (scaley+1)*16*scale:
            draw_decoration(deco, screen, dx, dy, scale)

def draw_building(building, screen, x, y, scale):
    """Dessine un bâtiment individuel."""
    size = building.size
    
    # Couleurs selon le type
    if building.type.startswith("domus"):
        color = (210, 180, 140)  # Tan
    elif building.type in ["forum", "basilica"]:
        color = (255, 255, 255)  # Blanc (marbre)
    elif building.type in ["temple", "sacellum"]:
        color = (255, 215, 0)  # Or
    elif building.type in ["horreum", "barn"]:
        color = (139, 90, 43)  # Brun
    else:
        color = (169, 169, 169)  # Gris
    
    # Dessiner le rectangle du bâtiment
    pygame.draw.rect(screen, color, 
                    (int(x), int(y), size[0] * 16 * scale, size[1] * 16 * scale))
    
    # Contour noir
    pygame.draw.rect(screen, (0, 0, 0), 
                    (int(x), int(y), size[0] * 16 * scale, size[1] * 16 * scale), 2)
    
    # Toit (triangle)
    roof_height = 8 * scale
    points = [
        (x, y),
        (x + size[0] * 16 * scale, y),
        (x + size[0] * 8 * scale, y - roof_height)
    ]
    pygame.draw.polygon(screen, (178, 34, 34), points)  # Rouge brique


def draw_decoration(deco, screen, x, y, scale):
    """Dessine une décoration."""
    if deco["type"] == "statue":
        pygame.draw.circle(screen, (200, 200, 200), (int(x), int(y)), 4 * scale)
    elif deco["type"] == "amphora":
        pygame.draw.circle(screen, (139, 69, 19), (int(x), int(y)), 2 * scale)
    elif deco["type"] == "fountain":
        pygame.draw.circle(screen, (100, 149, 237), (int(x), int(y)), 6 * scale)