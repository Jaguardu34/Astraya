from modules import variables as var
from modules import console as con

#ajouter un item a l'inventaire
def add_item(item, nb):
  for i in range(len(var.inventory)):
    if var.inventory[i][0] == item:
      var.inventory[i] = (item, var.inventory[i][1] + nb)
      return
  var.inventory.append((item, nb))

#enelever un item de l'inventaire
def remove_item(item, nb):
  for i in range(len(var.inventory)):
    if var.inventory[i][0] == item:
      var.inventory[i] = (item, var.inventory[i][1] - nb)
      if var.inventory[i][1] <= 0:
        var.inventory.pop(i)
      return

#return le nombre d'items dans l'inventaire
def item_in_inventory(item):
  for i in range(len(var.inventory)):
    if var.inventory[i][0] == item:
      return var.inventory[i][1]

  return 0
