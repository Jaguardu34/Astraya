import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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

WIDTH    = 1280	
HEIGTH   = 720
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

    # Grottes
    "rock": 10,
    "cave_ice": 11,
    "cave_mushroom": 12,
    "cave_normal": 13,
    "cave_crystal": 14,
    "cave_lava": 15,
    "air": 16
}

COLLIDE_TILES = [0, 7,70, 10, 15]  # ocean, mountains, snow_peak, collide

# textures
TEXTURES_PATH = os.path.join('Astraya2.0' ,'assets', 'textures', 'astrayatextures.png')
TEXTURE_MINIMAP_PATH = os.path.join('Astraya2.0', 'minimap.png')




# ==============================================================================
# TYPES DE BÂTIMENTS
# ==============================================================================

BUILDING_TYPES = {
    # Habitations
    "domus_modest": {"size": (3, 3), "rarity": "common"},
    "domus_rich": {"size": (4, 5), "rarity": "rare"},
    "villa_rustica": {"size": (6, 6), "rarity": "rare"},
    "insula": {"size": (4, 6), "rarity": "uncommon"},

    # Commerce
    "taberna": {"size": (2, 2), "rarity": "common"},
    "caupona": {"size": (3, 3), "rarity": "uncommon"},
    "macellum": {"size": (4, 4), "rarity": "uncommon"},
    "forum": {"size": (8, 8), "rarity": "very_rare"},

    # Stockage
    "horreum": {"size": (4, 4), "rarity": "common"},  # AJOUT
    "horreum_small": {"size": (2, 3), "rarity": "common"},
    "horreum_large": {"size": (4, 5), "rarity": "uncommon"},

    # Infrastructure
    "puteus": {"size": (1, 1), "rarity": "common"},
    "fornax": {"size": (2, 2), "rarity": "uncommon"},  # Forge
    "forge": {"size": (2, 2), "rarity": "uncommon"},   # AJOUT alias
    "balneum": {"size": (4, 4), "rarity": "rare"},
    "thermae": {"size": (6, 6), "rarity": "very_rare"},

    # Religion
    "sacellum": {"size": (2, 2), "rarity": "uncommon"},
    "temple": {"size": (5, 5), "rarity": "rare"},
    "altar": {"size": (1, 1), "rarity": "common"},
    "basilica": {"size": (7, 5), "rarity": "very_rare"},  # AJOUT

    # Militaire
    "castra": {"size": (8, 10), "rarity": "very_rare"},

    # Spectacle
    "amphitheatre": {"size": (10, 12), "rarity": "very_rare"},

    # Agricole
    "barn": {"size": (3, 2), "rarity": "common"},
}


# ==============================================================================
# TYPES DE VILLAGES
# ==============================================================================

nb_cities = 3

VILLAGE_TYPES = {
    "hamlet": {  # Hameau (4-6 maisons)
        "min_houses": 4,
        "max_houses": 6,
        "radius": 30,  # tiles
        "buildings": [
            ("domus_modest", 4, 6),  # (type, min, max)
            ("horreum_small", 1, 1),
            ("puteus", 1, 1),
            ("taberna", 0, 1),
            ("barn", 1, 2),
            ("altar", 1, 1),
        ]
    },
    
    "village": {  # Village moyen (10 maisons)
        "min_houses": 8,
        "max_houses": 12,
        "radius": 50,
        "buildings": [
            ("domus_modest", 8, 12),
            ("villa_rustica", 1, 1),
            ("caupona", 1, 1),
            ("fornax", 1, 1),
            ("macellum", 1, 1),
            ("sacellum", 1, 1),
            ("horreum_large", 1, 1),
            ("balneum", 0, 1),
            ("puteus", 1, 2),
        ]
    },
    
    "city": {  # Grande ville (20+ maisons)
        "min_houses": 20,
        "max_houses": 40,
        "radius": 80,
        "buildings": [
            ("domus_modest", 15, 25),
            ("domus_rich", 3, 5),
            ("insula", 5, 10),
            ("forum", 1, 1),
            ("basilica", 1, 1),
            ("thermae", 1, 1),
            ("temple", 1, 2),
            ("amphitheatre", 0, 1),
            ("castra", 1, 1),
            ("macellum", 2, 3),
            ("caupona", 3, 5),
            ("fornax", 2, 3),
            ("puteus", 3, 5),
        ]
    }
}