import pyxel
from modules import actions
from world_map import draw_map as dm
from game_part import menu, intro, settings, end
from modules import console as con
from modules import check_tiles as ct
from modules import player as p
from modules import ui
from modules import variables as var

#Initialisation de la fenetre
pyxel.init(var.windows_width,
           var.windows_height,
           title=" Astraya : The Awakening")


#lancer la boucle de jeu
def start():
  pyxel.run(update, draw)


  #Fonction mise a jour des frames
def update():
  if var.in_menu:
    menu.menu_update()
    return
  if var.in_introduction:
    intro.introduction_update()
    return
  if var.in_settings:
    settings.settings_update()
    return

  if var.end:
    end.end_update()
    return
  p.check_death()
  con.input()
  pyxel.mouse(True)
  if var.clock > 0:
    var.clock -= 1
  if var.delay > 0:
    var.delay -= 1
  if var.player_animation_timer > 0:
    var.player_animation_timer -= 1


#Fonction affichage
def draw():
  if var.in_menu:
    menu.menu_draw()
    return
  if var.in_introduction:
    intro.introduction_draw()
    return
  if var.in_settings:
    settings.settings_draw()
    return

  if var.end:
    end.end_draw()
    return
  if not var.death:
    ui.print_ui()
    dm.print_map(5, 5, 15, var.game_map, var.x, var.y)
    ui.print_coeur(var.coeur)
    con.print_console(160, 5, 235, 150)
    ui.print_inventory()
    actions.update_action()
    ui.triggers(6, 15)
  else:
    x = var.windows_width / 2 - 55
    y = var.windows_height / 2 + 50
    pyxel.cls(0)
    pyxel.text((var.windows_width - 9 * 4) // 2, (var.windows_height / 2) - 30,"GAME OVER", 8)
    pyxel.text((var.windows_width - 29 * 4) // 2, var.windows_height / 2,"Vous pouvez fermer la fenetre", 7)
    pyxel.rect(x, y, 110, 15, 7)
    pyxel.rectb(x, y, 110, 15, 0)
    pyxel.text(x+7, y+5, "Appuyer ici pour réesayer", 0)
    if pyxel.btnp(pyxel.KEY_T) or ui.check_click(x, y, 150, 20):
      var.in_menu  = True
      var.death = False
      var.coeur = 3
      var.x = 22
      var.y = 66
      var.current_quest = 0
      var.dialog_png_1_state = 0
      var.coeur = 10