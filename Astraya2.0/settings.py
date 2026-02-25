import os

SCALE = 2

WIDTH    = 1280	
HEIGTH   = 720
SCALE = 2
FPS      = 60
TILESIZE = 64
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

# textures
TEXTURES_PATH = os.path.join('Astraya2.0' ,'assets', 'textures', 'astrayatextures.png')
