import pyxel
from modules import ui
from modules import variables as var


#update le bouton de l'intro
def end_update():
    x = var.windows_width / 2 - 55
    y = var.windows_height / 2 + 50
    if pyxel.btnp(pyxel.KEY_T) or ui.check_click(x, y, 150, 20):
        quit()


#afficher l'intro
def end_draw():
    x = var.windows_width / 2 - 55
    y = var.windows_height / 2 + 50
    pyxel.cls(1)
    pyxel.blt(0, 0, 0, 0, 0, 200, 170)  ##background
    pyxel.blt(200, 0, 1, 0, 0, 200, 170)  ##autre partie du background
    pyxel.rect(((400-58*4)//2)-5, 45, 242, 60, 7)
    pyxel.rectb(((400-58*4)//2)-5, 45, 242, 60, 0)
    pyxel.text(((400-58*4)//2), 50, "Vous avez reussi a repondre au question du heros antique !", 0)
    pyxel.text(((400-32*4)//2),70, "Merci d'avoir jouer a notre jeu ", 0)
    pyxel.text(((400-21*4)//2),80, "Astraya reviendra ...", 0)
    

    pyxel.rect(x, y, 110, 15, 7)
    pyxel.rectb(x, y, 110, 15, 0)
    pyxel.text(x+7, y+5, "Appuyer ici pour quitter", 0)
