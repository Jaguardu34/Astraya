from modules import variables as var
from modules import inventory as inv
from modules import console as con
from modules import ui
import random
import pyxel

is_cutting = False
pos_actionbar = 0, 0

#update les actiond
def update_action():
  cut_tree()

#action couper arbre
def cut_tree():
  if inv.item_in_inventory("Hache") > 0:
    global is_cutting, pos_actionbar
    if pyxel.btn(pyxel.KEY_E):
      dx, dy = 0, 0
      if var.orientation == "face":
        dy = 1
        pos_actionbar = 80, 90
      elif var.orientation == "back":
        dy = -1
        pos_actionbar = 80, 70
      elif var.orientation == "left":
        dx = -1
        pos_actionbar = 70, 80
      elif var.orientation == "right":
        dx = 1
        pos_actionbar = 90, 80
      if var.game_map[var.y + dy][var.x + dx] in (25, 74, 75, 76):
        if not is_cutting:
          var.actionbar = 100
          is_cutting = True
        if is_cutting:
          var.actionbar -= 2

          if var.actionbar <= 0:
            is_cutting = False
            var.actionbar = 0
            var.game_map[var.y + dy][var.x + dx] = random.randint(1, 16)
            inv.add_item("Bois", 1)
      elif var.game_map[var.y + dy][var.x + dx] in (49, 50, 51, 52):
        if not is_cutting:
          var.actionbar = 100
          is_cutting = True
        if is_cutting:
          var.actionbar -= 2

          if var.actionbar <= 0:
            is_cutting = False
            var.actionbar = 0
            var.game_map[var.y + dy][var.x + dx] = random.randint(53, 56)
            inv.add_item("Bois", 1)
      pos_x, pos_y = pos_actionbar
      ui.print_actionbar(var.actionbar, pos_x, pos_y)
    else:
      is_cutting = False
      var.actionbar = 0
  else:
    if pyxel.btnp(pyxel.KEY_E):
      dx, dy = 0, 0
      if var.orientation == "face":
        dy = 1
      elif var.orientation == "back":
        dy = -1
      elif var.orientation == "left":
        dx = -1
      elif var.orientation == "right":
        dx = 1
      if var.game_map[var.y + dy][var.x + dx] in (25, 74, 75, 76, 49, 50, 51,52) and not is_cutting:
        con.print_to_console("Vous n'avez pas d'outil pour couper des arbres", 4)