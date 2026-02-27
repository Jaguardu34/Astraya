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

texture_chicken = create_texture_mirrored(0, 48, 3)
texture_player  = create_texture_basic(0, 80, 1)

texture_coeur = get_sprite(sprite_sheet, 0, 241, 16, 16)
texture_coeur_upscaled = pygame.transform.scale(texture_coeur, (texture_coeur.get_width()*  SCALE, texture_coeur.get_height()*  SCALE))  

texture_grotte = create_single_texture_by_coords(100, 100, 0, 0)