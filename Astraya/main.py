from modules import game
import os
import pyxel
from modules import maze
# Dossier où se trouve main.py
asset_path = os.path.join(os.path.dirname(__file__), "assets")

# Chargement des images Pyxel
pyxel.images[0].load(0, 0, os.path.join(asset_path, "background_left.png"))
pyxel.images[1].load(0, 0, os.path.join(asset_path, "background_right.png"))
pyxel.images[2].load(0, 0, os.path.join(asset_path, "image_bank.png"))

#generele le labyrinthe
maze.generate_maze(30, 14)  ##generation du labyrinthe

#lancer le jeu
game.start()

print("Jeu lancé")
