import pyxel
from modules import ui
from modules import variables as var

#update le menu
def menu_update():
  pyxel.mouse(True)
  x = var.windows_width / 2 - 25
  y = var.windows_height / 2 - 10
  y_2 = var.windows_height / 2 + 25

  if pyxel.btnp(pyxel.KEY_T) or ui.check_click(x, y, 50, 20):
    var.in_menu = False
    var.in_introduction = True

  if ui.check_click(x, y_2, 50, 20):
    var.in_menu = False
    var.in_settings = True

#afficher le menu
def menu_draw():
  x = var.windows_width / 2 - 25
  y = var.windows_height / 2 - 10
  y_2 = var.windows_height / 2 + 25

  pyxel.cls(0)  ##couleur de fond
  pyxel.blt(0, 0, 0, 0, 0, 200, 170)  ##background
  pyxel.blt(200, 0, 1, 0, 0, 200, 170)  ##autre partie du background
  pyxel.text(var.windows_width / 3, 20, "Island Escape v0.11.12.2025.-01.11",
             0)

  pyxel.rect(x, y, 50, 20, 7)  ##rectangle du bouton
  pyxel.rectb(x, y, 50, 20, 0)  ##bordure du bouton
  pyxel.text(x + 17, y + 7, "Play", 0)  ##texte du bouton

  pyxel.rect(x, y_2, 50, 20, 7)  ##rectangle du bouton
  pyxel.rectb(x, y_2, 50, 20, 0)  ##bordure du bouton
  pyxel.text(x + 8, y_2 + 7, "Settings", 0)  ##texte du bouton