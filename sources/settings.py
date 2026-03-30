import os
import pygame
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
PLAYER_PLACE_RANGE = 5
#keys
KEY_UP = pygame.K_z
KEY_DOWN = pygame.K_s
KEY_LEFT = pygame.K_q
KEY_RIGHT = pygame.K_d
KEY_MAP = pygame.K_TAB
KEY_MENU = pygame.K_ESCAPE
KEY_INVENTORY = pygame.K_e
KEY_DROP = pygame.K_g
KEY_NPC = pygame.K_a

WINDOW_WIDTH    = 1280
WINDOW_HEIGTH   = 720
FPS      = 60
TILE_SIZE = 32
HITBOX_OFFSET = {
	'player': -6,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors

# ui colors
HEALTH_COLOR = 'red'
HOTBAR_ACTIVE = 'gold'

#world_gen
SIZE = 2000
NB_VILLAGES = 80
SEED = 0

# Encodage des biomes en IDs numériques pour NumPy
BIOME_IDS = {
    "ocean": 0,
    "beach": 1,
    "wet_sand" : 101,
    "plains": 2,
    "jungle": 3,
    "forest": 4,
    "mountains": 5,
    "snow_peak": 6,
    "collide": 7,
    "donjon_collide": 71,
    "cliff_N":701,
    "cliff_E":702,
    "cliff_S":703,
    "cliff_O":704,
    "cliff_NO":705,
    "cliff_NE":706,
    "cliff_SE":707,
    "cliff_SO":708,
    "passage_cliff_N_1":709,
    "passage_cliff_N_2":710,
    "passage_cliff_E_1":711,
    "passage_cliff_E_2":712,
    "passage_cliff_S_1":713,
    "passage_cliff_S_2":714,
    "passage_cliff_O_1":715,
    "passage_cliff_O_2":716,
    "corrupted": 800,

    # Grottes
    "rock": 10,
    "cave_ice": 11,
    "cave_mushroom": 12,
    "cave_normal": 13,
    "cave_crystal": 14,
    "cave_lava": 15,
    "air": 16
}

COLLIDE_TILES = [0, 7,70,71, 10, 15]  # ocean, mountains, snow_peak, collide

# textures
TEXTURES_PATH = os.path.join('sources' ,'assets', 'textures', 'astraya_textures_final.png')
TEXTURE_MINIMAP_PATH = os.path.join('sources', 'minimap.png')




# Biomes interdits pour les villages (eau et sable)
FORBIDDEN_VILLAGE_BIOMES = [
    BIOME_IDS["ocean"],      # 0
    BIOME_IDS["beach"],      # 1
    BIOME_IDS["wet_sand"],   # 101
]

#random building version
def random_temple():
    templescoords=[(0,1920),(160,1920),(0,2080),(160,2080)]
    r=random.randint(0,3)
    return templescoords[r]
# ==============================================================================
# TYPES DE BÂTIMENTS (6 types seulement)
# ==============================================================================

BUILDING_TYPES = {
    "domus": {"size": (3, 3), "rarity": "common","xycoord":(0,0)},

    "villa": {"size": (5, 5), "rarity": "rare","xycoord":(192,224)},

    "forum": {"size": (8, 8), "rarity": "common","xycoord":(0,832)},

    # Stockage
    "stock": {"size": (3, 3), "rarity": "common","xycoord":(0,608)},

    "temple": {"size": (5, 5), "rarity": "uncommon","xycoord":random_temple()},

    "puteus": {"size": (1, 1), "rarity": "common","xycoord":(0,1633)},
}


# ====================
# TYPES DE VILLAGES
# ====================

nb_cities = 3

VILLAGE_TYPES = {
    "hamlet": {  # Hameau (5-8 maisons)
        "min_houses": 5,
        "max_houses": 8,
        "radius": 40,  # tiles
        "buildings": [
            ("domus", 5, 8),        # Maisons simples
            ("stock", 1, 2),      # Stockage
            ("puteus", 1, 1),       # Puits central
        ]
    },

    "city": {  # Grande ville (20-35 bâtiments)
        "min_houses": 20,
        "max_houses": 35,
        "radius": 80,
        "buildings": [
            ("domus", 15, 25),      # Maisons simples
            ("villa", 2, 5),        # Maisons riches
            ("forum", 1, 1),        # Place du marché
            ("temple", 1, 2),       # Temple
            ("stock", 2, 4),      # Stockages
            ("puteus", 2, 3),       # Puits
        ]
    }
}
