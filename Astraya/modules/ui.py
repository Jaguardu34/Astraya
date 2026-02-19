import pyxel
from modules import variables as var


def print_ui():
  pyxel.cls(var.background_color)
  pyxel.rect(0, var.windows_height - 10, var.windows_width, 10, 15)


#Fonction affichage coeur
def print_coeur(nbcoeur):

  def coeur(x, y):
    pyxel.rect(x - 1, y - 2, 1, 1, 8)
    pyxel.rect(x + 1, y - 2, 1, 1, 8)
    pyxel.rect(x - 2, y - 1, 5, 1, 8)
    pyxel.rect(x - 1, y, 3, 1, 8)
    pyxel.rect(x, y + 1, 1, 1, 8)

  for i in range(nbcoeur):
    coeur(5 + i * 7, var.windows_height - 5)


#verifier si un bouton est clique
def check_click(nx, ny, widht, height):
  if pyxel.btnp(
      pyxel.MOUSE_BUTTON_LEFT
  ) and pyxel.mouse_x >= nx and pyxel.mouse_x <= nx + widht and pyxel.mouse_y >= ny and pyxel.mouse_y <= ny + height:
    return True


#afficher l'inventaire
def print_inventory():
  if var.inventory:
    for i in range(len(var.inventory)):
      item, nb = var.inventory[i]
      if item == "Bois":
        pyxel.blt(80 + 30 * i, var.windows_height - 10, 2, 20, 0, 10, 10, 0)
        pyxel.text(80 + (30 * i) + 12, var.windows_height - 8, f"{nb}", 0)
      elif item == "Hache":
        pyxel.blt(80 + 30 * i, var.windows_height - 10, 2, 0, 153, 10, 10, 0)
        pyxel.text(80 + (30 * i) + 12, var.windows_height - 8, f"{nb}", 0)
      elif item == "Ski":
        pyxel.blt(80 + 30 * i, var.windows_height - 10, 2, 11, 153, 10, 10, 0)
        pyxel.text(80 + (30 * i) + 12, var.windows_height - 8, f"{nb}", 0)
      else:

        pyxel.text(80 + 40 * i + 12, var.windows_height - 8, f"{item}: {nb}",
                   0)


#afficher la barre d'action
def print_actionbar(nb, x, y):
  if nb > 0:
    pyxel.rect(x - 5, y - 1, 10, 2, 7)
    pyxel.rect(x - 5, y - 1, (nb * 10) / 100, 2, 13)


#afficher les triggers
def triggers(x, y):
  if var.current_quest == 0:
    pyxel.text(x, y, "Parler au pecheur", 2)
  elif var.current_quest == 1:
    pyxel.text(x, y, "Trouver le village", 2)
  elif var.current_quest == 2:
    if var.dialog_png_1_state == 0:
      pyxel.text(x, y, "Parler a Roger", 2)
    else:
      pyxel.text(x, y, "Ramener du bois a Roger", 2)

  elif var.current_quest == 3:
    pyxel.text(x, y, "Trouver Helena", 2)

  elif var.current_quest == 4:
    pyxel.text(x, y, "Trouver la statue", 2)
