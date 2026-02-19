from world_map.generate_map import create_map
# états du jeu
in_menu = True
in_introduction = False
in_console = False
in_settings = False
death = False

# paramètres de la fenêtre
windows_width = 400  # largeur par défaut de la fenêtre
windows_height = 170  # hauteur par défaut de la fenêtre
background_color = 7
text_color = 0

# joueur
x = 22
y = 66
coeur = 10
collide = False

# collisions & interactions
tiles_collide = [
    17, 18, 19, 20, 25, 31, 32, 44, 45, 46, 47, 68, 69, 74, 75, 76, 49, 50, 51,
    52, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
    114, 115, 116, 96, 98
]
tile_interaction = [300, 301]

# temps / logique
clock = 0
delay = 0

## map
game_map = create_map(80, 80)

consoleinfo = 0, 0, 100, 100
console_lines = []  #Contenu de la console meme pas affiché
console_content = ""  #Contenu de l'input de l'utilisateur
pos_cursor = 0  #Position curseur
timer_cursor = 0
player_name = ""

#console
in_name_input = False
dialog_step = 0

#dialogs
current_dialog = 0

inventory = []

actionbar = 0

#player
player_animation_timer = 0
orientation = "face"

#dialogs
dialog_png_1_state = 0
dialog_hero_state = 0
hero_question_posed = False
#quetes
current_quest = 0

end = False
