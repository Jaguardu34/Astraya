import pyxel
from modules import ui
from modules import variables as var


#update le bouton de l'intro
def introduction_update():
    x = var.windows_width / 2 - 75
    y = var.windows_height / 2 + 50
    if pyxel.btnp(pyxel.KEY_T) or ui.check_click(x, y, 150, 20):
        var.in_introduction = False
    if pyxel.btnp(pyxel.KEY_SPACE):
        var.in_menu = True
        var.in_introduction = False


#afficher l'intro
def introduction_draw():
    x = var.windows_width / 2 - 75
    y = var.windows_height / 2 + 50
    pyxel.cls(1)
    pyxel.blt(0, 0, 0, 0, 0, 200, 170)  ##background
    pyxel.blt(200, 0, 1, 0, 0, 200, 170)  ##autre partie du background
    pyxel.rect(25, 5, 350, 100, 7)
    pyxel.rectb(25, 5, 350, 100, 0)
    pyxel.text(
        30, 10,
        "Bienvenue a Astraya, une ile apparemment perdue au milieu de l'ocean Atlantique",
        0)
    pyxel.text(30, 30, "Ou seuls des naufrages ont deja mis les pieds.", 0)
    pyxel.text(
        30, 50,
        "Vous vous reveillez sur une plage, sans souvenir de comment vous etes arrive.",
        0)
    pyxel.text(30, 70,
               "Quelque chose de terrible s'est produit sur cette ile...", 0)
    pyxel.text(30, 90, "Appuyer sur ESPACE pour revenir en arriere", 0)
    pyxel.rect(x, y, 150, 20, 7)
    pyxel.rectb(x, y, 150, 20, 0)
    pyxel.text(x + 17, y + 7, "Cliquer ici pour vous reveiller", 0)
