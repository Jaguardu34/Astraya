import pyxel
from modules import ui
from modules import variables as var


def settings_update():
  if pyxel.btnp(pyxel.KEY_SPACE):
    var.in_menu = True
    var.in_settings = False


def settings_draw():
  pyxel.cls(1)
  pyxel.blt(0, 0, 0, 0, 0, 200, 170)  ##background
  pyxel.blt(200, 0, 1, 0, 0, 200, 170)  ##autre partie du background
  pyxel.text(180, 10, "Parametres", 0)
  pyxel.text(122, 30, "Appuyez sur ESPACE pour revenir au menu", 0)
  pyxel.rect(87, 52, 225, 55, 7)
  pyxel.rectb(87, 52, 225, 55, 0)
  pyxel.text(104, 57,  "Utilisez ZQSD ou les fleches pour vous deplacer.", 0)
  pyxel.text(114, 67,  "Utilisez E pour interagir avec les objets.", 0)
  pyxel.text(92,  77,  "Utilisez shift pour envoyer le message dans la console", 0)
  pyxel.text(120, 87,  "Utilisez CTRL + T pour ouvrir la console.", 0)
  pyxel.text(120, 97,  "Utilisez CTRL + C pour fermer la console.", 0)