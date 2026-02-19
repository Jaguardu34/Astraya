from modules import variables as var
from modules import console as con
from modules import inventory as inv


# fonctions dialogs
def dialogs(n):
  var.current_dialog = n

  if n == 2:  # Pecheur
    if var.current_quest == 0:
      var.console_lines = []
      con.print_to_console("Bonjour naufrage, je m'appelle Fisher.", 7)
      con.print_to_console("Bienvenue a Astraya, quel est ton nom ?", 7)
      var.in_console = True
      var.current_quest = 1
    elif var.current_quest == 1:
      var.console_lines = []
      con.print_to_console(f"Bonjour {var.player_name}", 7)
      con.print_to_console("Suis les pommiers et tu arriveras au village", 7)
      con.print_to_console("La-bas tu trouveras le chef du village", 7)
    else:
      var.console_lines = []
      con.print_to_console(f"Bonjour {var.player_name}", 7)

  elif n == 5:  # Chef
    if var.current_quest == 1:
      var.console_lines = []
      con.print_to_console("Bonjour jeune homme, je suis le chef du village.",
                           7)
      con.print_to_console("Veux-tu savoir l'histoire de cette ile ?", 7)
      var.dialog_step = 0
      var.in_console = True
    else:
      con.print_to_console("é", 7)
      con.print_to_console("Bonjour jeune homme.", 7)

  elif n == 1:  # Roger
    if var.current_quest == 2:
      if var.dialog_png_1_state == 0:
        con.print_to_console("Bonjour jeune voyageur, je m'appelle Roger !", 7)
        con.print_to_console("Ma maison a ete detruite.", 7)
        con.print_to_console(
            "Il me faudrait 10 buches de bois pour la reparer.", 7)
        con.print_to_console(
            "Tu peux te mettre face a un arbre avec une hache et appuyer sur E pour le couper !",
            7)
        con.print_to_console(
            "Pourrais-tu aller me chercher ca, s'il te plait ?", 7)
        var.in_console = True
      else:
        if inv.item_in_inventory("Bois") >= 10:
          con.print_to_console("Merci beaucoup pour le bois !", 7)
          con.print_to_console(
              "Suis ce chemin pour trouver Helena, c'est la guardienne du labyrinth.",
              7)
          con.print_to_console(
              "Elle pourrait d'aider a atteindre les montagnes.", 7)
          inv.remove_item("Bois", 10)
          var.current_quest = 3
        else:
          con.print_to_console("é", 7)
          con.print_to_console("Tu n'as pas assez de bois.", 7)

    elif var.current_quest > 2:
      con.print_to_console("é", 7)
      con.print_to_console("Bonjour jeune voyageur !", 7)
    else:
      con.print_to_console("Qui es-tu ? Va parler au chef du village !", 7)

  elif n == 3:  # Helena
    if var.current_quest == 3:
      var.console_lines = []
      con.print_to_console("Bien le bonjour, jeune homme, je suis Helena.", 7)
      con.print_to_console("J'ai une enigme pour toi :", 7)
      con.print_to_console(
          "Je glisse sans roues et avance grace a ton équilibre ,", 7)
      con.print_to_console(
          "On me fixe aux pieds pour dompter la neige et la pente,", 7)
      con.print_to_console(
          "Sans moi, la montagne d’hiver devient un mur infranchissable.", 7)
      var.in_console = True
    elif var.current_quest > 3:
      con.print_to_console("Va voir au-dela de la montagne.", 7)
    else:
      con.print_to_console("é", 7)
      con.print_to_console(
          "Je ne te dirai rien tant que tu n'auras pas aider Roger", 7)

  elif n == 100:  # Hero
    if var.current_quest == 4:
      if var.dialog_hero_state == 0:
        var.console_lines = []
        con.print_to_console("Je suis le heros de cette ile.", 7)
        con.print_to_console(
            "Si tu veux gagner ta place sur l'ile, il faudra repondre a ces quatres questions.",
            7)
        con.print_to_console("Es-tu pret ?", 7)
        con.print_to_console("Premiere question :", 7)
        con.print_to_console(
            "Quel est le nom du premier peuple de cette ile ?", 7)
        var.hero_question_posed = True
      elif var.dialog_hero_state == 1:
        con.print_to_console("Deuxieme question :", 7)
        con.print_to_console("Quel est le nom du pecheur de l'ile ?", 7)
        var.hero_question_posed = True
      elif var.dialog_hero_state == 2:
        con.print_to_console("Troisieme question :", 7)
        con.print_to_console("Comment s'appelle la gardienne du labyrinthe ?",
                             7)
        var.hero_question_posed = True
      elif var.dialog_hero_state == 3:
        con.print_to_console("Derniere question :", 7)
        con.print_to_console("Combien y a-t-il de villageois sur l'ile ?", 7)
        var.hero_question_posed = True
    else:
      con.print_to_console("é", 7)
      con.print_to_console("Tu n'as pas assez de connaissances pour repondre a mes questions.", 7)
