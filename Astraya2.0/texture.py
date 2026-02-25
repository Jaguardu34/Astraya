import pygame
import os
import settings


textures = pygame.image.load(os.path.join('Astraya2.0' ,'assets', 'textures', 'astrayatextures.png'))

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

def create_texture_basic(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(textures, posx + (i * 16), posy, 16, 16))
    
    tab_upscaled = []
    for i in range(len(tab)):
        tab_upscaled.append(pygame.transform.scale(tab[i], (tab[i].get_width() * settings.SCALE, tab[i].get_height()*settings.SCALE)))
        
    return tab_upscaled

def create_texture_mirrored(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(textures, posx + (i * 16), posy, 16, 16))
    
    tab_upscaled = []
    for i in range(len(tab)):
        tab_upscaled.append(pygame.transform.scale(tab[i], (tab[i].get_width() * settings.SCALE, tab[i].get_height()*settings.SCALE)))
        
    for i in range(len(tab)):
        tab_upscaled.append(pygame.transform.flip(tab_upscaled[i], True, False))
        
    return tab_upscaled
        

def create_texture_with_rotation(posx, posy, nbr):
    tab = []
    for i in range(nbr):
        tab.append(get_sprite(textures, posx + (i * 16), posy, 16, 16))
        tab.append(pygame.transform.rotate(get_sprite(textures, posx + (i * 16), posy, 16, 16), 90))
        tab.append(pygame.transform.rotate(get_sprite(textures, posx + (i * 16), posy, 16, 16), -90))
        tab.append(pygame.transform.rotate(get_sprite(textures, posx + (i * 16), posy, 16, 16), 180))
    
    tab_upscaled = []
    for i in range(len(tab)):
        tab_upscaled.append(pygame.transform.scale(tab[i], (tab[i].get_width() * settings.SCALE, tab[i].get_height()*settings.SCALE)))
        
    return tab_upscaled


texture_herbe_upscaled = create_texture_with_rotation(0, 0, 4)
texture_sand_upscaled = create_texture_with_rotation(0, 16, 4)

texture_chicken = create_texture_mirrored(0, 48, 3)
