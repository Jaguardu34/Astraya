import pygame
from settings import *



sprite_sheet = pygame.image.load(TEXTURES_PATH)

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

def create_texture_basic(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(sprite_sheet, posx + (i * 32), posy, 32, 32))
    
    return tab

def create_texture_mirrored(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(sprite_sheet, posx + (i * 32), posy, 32, 32))
    
    tab_return = []
        
    for i in range(len(tab)):
        tab_return.append(pygame.transform.flip(tab[i], True, False))
        
    return tab_return
        

def create_texture_with_rotation(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(sprite_sheet, posx + (i * 32), posy, 32, 32))
        tab.append(pygame.transform.rotate(get_sprite(sprite_sheet, posx + (i * 32), posy, 32, 32), 90))
        tab.append(pygame.transform.rotate(get_sprite(sprite_sheet, posx + (i * 32), posy, 32, 32), -90))
        tab.append(pygame.transform.rotate(get_sprite(sprite_sheet, posx + (i * 32), posy, 32, 32), 180))

        
    return tab

def create_single_texture_by_coords(x, y, w, h):
    
    texture = [get_sprite(sprite_sheet, x, y, w, h)]
        

    return texture
    


texture_herbe = create_texture_with_rotation(0, 0, 4)
texture_sand = create_texture_with_rotation(0, 64, 4)
texture_wet_wand = create_texture_with_rotation(128, 64, 4)

texture_player  = create_texture_basic(0, 80, 1)


texture_coeur = get_sprite(sprite_sheet, 0, 241, 16, 16)
texture_coeur_upscaled = pygame.transform.scale(texture_coeur, (texture_coeur.get_width()*  SCALE, texture_coeur.get_height()*  SCALE))  

texture_grotte = create_single_texture_by_coords(100, 100, 0, 0)

texture_chicken_base = [get_sprite(sprite_sheet, 0, 112, 16, 16), get_sprite(sprite_sheet, 0, 96, 16, 16), get_sprite(sprite_sheet, 16, 96, 16, 16), 
                   pygame.transform.flip(get_sprite(sprite_sheet, 0, 112, 16, 16), True, False),
                   pygame.transform.flip(get_sprite(sprite_sheet, 0, 96, 16, 16), True, False),
                   pygame.transform.flip(get_sprite(sprite_sheet, 16, 96, 16, 16), True, False)]

texture_chicken = []
for i in range(len(texture_chicken_base)):
    texture_chicken.append(pygame.transform.scale(texture_chicken_base[i], (texture_chicken_base[i].get_width() * 1.5, texture_chicken_base[i].get_height()* 1.5)))


# CHANGEMENT : Utilisation d'IDs numériques au lieu de strings pour correspondre à map.BIOME_IDS
TILE_COLORS = {
    0: (0, 76, 153),      # ocean - ID 0 au lieu de "ocean"
    1: (237, 201, 120),   # sand
    2: (100, 180, 80),  
    101: (255, 0, 0),
    3: (144, 238, 144),   # jungle - ID 3 au lieu de "jungle"
    4: (0, 100, 0),       # forest - ID 4 au lieu de "forest"
    5: (128, 128, 128),   # mountains - ID 5 au lieu de "mountains"
    6: (255, 255, 255),   # snow_peak - ID 6 au lieu de "snow_peak"
    7: (255, 0, 0),       # collide - ID 7 au lieu de "collide"
    10: (50, 50, 50),     # rock - ID 10 au lieu de "rock"
    11: (180, 220, 255),  # cave_ice - ID 11 au lieu de "cave_ice"
    12: (150, 0, 150),    # cave_mushroom - ID 12 au lieu de "cave_mushroom"
    13: (120, 120, 120),  # cave_normal - ID 13 au lieu de "cave_normal"
    14: (0, 200, 255),    # cave_crystal - ID 14 au lieu de "cave_crystal"
    15: (255, 80, 0),     # cave_lava - ID 15 au lieu de "cave_lava"
}

# CHANGEMENT : IDs numériques pour les textures
TILE_TEXTURE = {
    2: texture_herbe,  # plains - ID 2 au lieu de "plains"
    1: texture_sand,    # beach - ID 1 au lieu de "beach"
    101: texture_wet_wand
}

texture_ocean = create_texture_basic(0, 128, 4)  

TILE_ANIMATED = {
    0: texture_ocean,   # ocean animé
}