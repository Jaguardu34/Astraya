import pygame
from settings import *
import os
import random



sprite_sheet = pygame.image.load(TEXTURES_PATH)
sprite_sheet_terrain = pygame.image.load(os.path.join('sources' ,'assets', 'textures', 'astraya_textures_final.png'))


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
        tab_return.append(tab[i])
        tab_return.append(pygame.transform.flip(tab[i], True, False))

    return tab_return


def create_texture_with_rotation(posx, posy, cols=1, rows=1, chance=1, rotation=True):
    """
    posx, posy : en pixel
    cols, rows : nombre de colonnes et de lignes de textures à charger
    chance     : nombre de fois que chaque texture est dupliquée (augmente la probabilité d'apparition)
    rotation   : si True, génère aussi les rotations 90, 180, 270
    """
    tab = []
    for row in range(rows):
        for col in range(cols):
            sprite = get_sprite(sprite_sheet, posx + (col * 32), posy + (row * 32), 32, 32)

            tab.extend([sprite] * chance)
            if rotation:
                tab.extend([pygame.transform.rotate(sprite, 90)]  * chance)
                tab.extend([pygame.transform.rotate(sprite, 180)] * chance)
                tab.extend([pygame.transform.rotate(sprite, -90)] * chance)

    return tab

def create_single_texture_by_coords(sheet,x, y, w, h):

    texture = [get_sprite(sheet, x, y, w, h)]


    return texture

###################SONNNSSNNSNSNSNSNSN##################################
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sound_path = "sources/assets/sound/"

sound_chicken = pygame.mixer.Sound(sound_path+ "sound_disign/poule.mp3")
sound_chicken.set_volume(0.1)

sound_fermier_bonjour = pygame.mixer.Sound(sound_path+"sound_disign/js_fermier.wav")
sound_fermier_aurevoir = pygame.mixer.Sound(sound_path+"sound_disign/bonne_journe.mp3")
######################################################################
texture_herbe = create_texture_basic(96, 0, 1)
texture_sand = create_texture_basic(192, 0, 4)
texture_wet_wand = create_texture_basic(384, 0 ,4)
texture_forest = create_texture_basic(0, 0, 1)

texture_old_npc = create_texture_basic(0, 320, 1)

texture_plant = create_texture_basic(0, 64, 9)
#+ create_texture_with_rotation(posx =128, posy = 384, cols=4, rows=4, rotation=False, chance=1)

texture_boss = [get_sprite(sprite_sheet, 0, 448, 160, 130), get_sprite(sprite_sheet, 176, 448, 160, 140)]

texture_player = [
    get_sprite(sprite_sheet, 0,  320, 13, 35),
    get_sprite(sprite_sheet, 15, 320, 17, 34),
    get_sprite(sprite_sheet, 32, 320, 14, 36),
    pygame.transform.flip(get_sprite(sprite_sheet, 0,  320, 13, 35), True, False),
    pygame.transform.flip(get_sprite(sprite_sheet, 15, 320, 17, 34), True, False),
    pygame.transform.flip(get_sprite(sprite_sheet, 32, 320, 14, 36), True, False),
    get_sprite(sprite_sheet, 51,  320, 14, 36),
    get_sprite(sprite_sheet, 66, 320, 15, 36),
    get_sprite(sprite_sheet, 83, 320, 13, 36),
    get_sprite(sprite_sheet, 97,  320, 16, 36),
    get_sprite(sprite_sheet, 113, 320, 15, 38),
    get_sprite(sprite_sheet, 129, 320, 15, 38),
]

texture_swipe_weapon = create_texture_basic(0, 896, 1)


texture_grotte = create_single_texture_by_coords(sprite_sheet_terrain,0, 143, 32, 32)

texture_chicken_base = [get_sprite(sprite_sheet, 0, 304, 16, 16), get_sprite(sprite_sheet, 0, 288, 16, 16), get_sprite(sprite_sheet, 16, 288, 16, 16),
                   pygame.transform.flip(get_sprite(sprite_sheet, 0, 304, 16, 16), True, False),
                   pygame.transform.flip(get_sprite(sprite_sheet, 0, 288, 16, 16), True, False),
                   pygame.transform.flip(get_sprite(sprite_sheet, 16, 288, 16, 16), True, False)]

texture_oeuf = [get_sprite(sprite_sheet, 16, 304, 16, 16)]

texture_coeur = [get_sprite(sprite_sheet, 0, 926, 16, 16), get_sprite(sprite_sheet, 16, 926, 16, 16), get_sprite(sprite_sheet, 0, 942, 16, 16)]

texture_chicken = []
for t in texture_chicken_base:
    texture_chicken.append(pygame.transform.scale(t, (
        int(t.get_width() * 1.5),
        int(t.get_height() * 1.5)
    )))

texture_chicken_corrupted_base = [get_sprite(sprite_sheet, 0, 240, 16, 16), get_sprite(sprite_sheet, 0, 224, 16, 16), get_sprite(sprite_sheet, 16, 224, 16, 16),
                   pygame.transform.flip(get_sprite(sprite_sheet, 0, 240, 16, 16), True, False),
                   pygame.transform.flip(get_sprite(sprite_sheet, 0, 224, 16, 16), True, False),
                   pygame.transform.flip(get_sprite(sprite_sheet, 16, 224, 16, 16), True, False)]

texture_chicken_corrupted = []
for t in texture_chicken_corrupted_base:
    texture_chicken_corrupted.append(pygame.transform.scale(t, (
        int(t.get_width() * 1.5),
        int(t.get_height() * 1.5)
    )))

texture_tree = [pygame.transform.scale(get_sprite(sprite_sheet, 0, 96, 32, 32), (64, 64))]

texture_cow_base = create_texture_mirrored(32, 288, 3)
texture_cow = []
for t in texture_cow_base:
    texture_cow.append(pygame.transform.scale(t, (
        int(t.get_width() * 1.5),
        int(t.get_height() * 1.5)
    )))

texture_fermier = create_texture_basic(64, 320, 1)

TILE_COLORS = {
    0: (0, 76, 153),      # ocean - ID 0 au lieu de "ocean"
    1: (237, 201, 120),   # sand
    2: (100, 180, 80),
    101: (237, 201, 120),
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
    71: (133, 34, 155),     # donjon_collide - ID 71 au lieu de "donjon_collide"
    800: (178, 102 , 255)
}

# CHANGEMENT : IDs numériques pour les textures
TILE_TEXTURE = {
    2: texture_herbe,  # plains - ID 2 au lieu de "plains"
    1: texture_sand,   # beach - ID 1 au lieu de "beach"
    4 : texture_forest, # jungle - ID 3 au lieu de "jungle"
    101: texture_wet_wand,
}

BLOCK_TEXTURE ={
    2: texture_herbe,  # plains - ID 2 au lieu de "plains"
    1: texture_sand,    # beach - ID 1 au lieu de "beach"
    101: texture_wet_wand
}

texture_ocean = create_texture_basic(576, 0, 4)

TILE_ANIMATED = {
    0: texture_ocean,   # ocean animé
}

cliff_plain = create_texture_with_rotation(32,0, cols=1, rows=1, rotation=True)
cliff_forest_diagonal = create_texture_with_rotation(64,0, cols=1, rows=1, rotation=True)

cliff_forest = create_texture_with_rotation(128,0, cols=1, rows=1, rotation=True)
cliff_plain_diagonal = create_texture_with_rotation(192,0, cols=1, rows=1, rotation=True)


TILE_EDGE = {
    (2, "N"): cliff_plain[0],  # plains ID=2
    (2, "S"): cliff_plain[2],
    (2, "E"): cliff_plain[3],
    (2, "O"): cliff_plain[1],

    # etc.
}
