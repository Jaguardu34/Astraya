from modules import variables as var
## Vérification de la mort du joueur
def check_death():
  if var.coeur <= 0:
    var.death = True