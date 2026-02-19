import pyxel
from modules import variables as var
from modules import console as con
from modules import player as p
from modules.variables import x, y
from modules import dialogs as dial
from modules import inventory as inv


##Récupérer la tile à une position donnée
def get_tile(x, y):
  if y < 0 or y >= len(var.game_map):
    return -1
  if x < 0 or x >= len(var.game_map[y]):
    return -1
  return var.game_map[y][x]


#Verfier si les déplacements sont possibles
def try_move(nx, ny):

  tile = int(get_tile(nx, ny))

  if tile in var.tiles_collide or tile == -1:
    var.collide = True
    pyxel.play(0, 0)
    return False  #Chatgpt pour le return False

  if tile == 27:  # pêcheur
    var.collide = True
    dial.dialogs(2)

    return False

  if tile == 30:  # chef du village
    var.collide = True
    dial.dialogs(5)

    return False

  if tile == 26:  # Roger
    var.collide = True
    dial.dialogs(1)

    return False

  if tile == 28:  # Helena
    var.collide = True
    dial.dialogs(3)
    return False

  if tile == 48:  # hero en ruine
    var.collide = True
    dial.dialogs(100)
    return False

  if tile in (70, 71, 72, 73):
    if inv.item_in_inventory("Ski") == 0:
      var.collide = True
      con.print_to_console("Vous n'avez pas de ski pour monter la montagne", 4)
      return False

  var.collide = False
  var.x = nx
  var.y = ny

  return True
