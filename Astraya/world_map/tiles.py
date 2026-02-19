import pyxel


def rot(x, y, o):
    if o == 0:
        return x, y
    elif o == 1:
        return 9 - y, x
    elif o == 2:
        return 9 - x, 9 - y
    elif o == 3:
        return y, 9 - x


## HERBES
def herbe(x, y, o):
    pyxel.rect(x, y, 10, 10, 11)
    px, py = rot(2, 1, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(5, 3, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(8, 6, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(1, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(3, 3, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(7, 1, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(6, 8, o)
    pyxel.pset(x + px, y + py, 3)


def herbe_var1(x, y, o):
    pyxel.rect(x, y, 10, 10, 11)
    px, py = rot(0, 3, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(4, 1, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(9, 5, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 8, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(2, 6, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(5, 4, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(8, 2, o)
    pyxel.pset(x + px, y + py, 3)


def herbe_var2(x, y, o):
    pyxel.rect(x, y, 10, 10, 11)
    px, py = rot(3, 2, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 4, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(1, 5, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(7, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(4, 8, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(0, 1, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(9, 3, o)
    pyxel.pset(x + px, y + py, 3)


def herbe_var3(x, y, o):
    pyxel.rect(x, y, 10, 10, 11)
    px, py = rot(2, 2, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(5, 6, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(8, 3, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(3, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(1, 8, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 1, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(7, 5, o)
    pyxel.pset(x + px, y + py, 3)
    px, py = rot(4, 4, o)
    pyxel.pset(x + px, y + py, 3)


## POTION
def potion(x, y):
    pyxel.rect(x, y, 10, 10, 13)
    pyxel.rect(x + 3, y + 5, 4, 5, 6)
    pyxel.rect(x + 2, y + 6, 6, 3, 6)
    pyxel.rect(x + 4, y + 1, 2, 9, 6)
    pyxel.rect(x + 3, y + 2, 4, 1, 6)
    pyxel.rect(x + 4, y + 1, 2, 1, 10)
    pyxel.rect(x + 4, y + 2, 2, 7, 2)
    pyxel.rect(x + 3, y + 6, 4, 3, 2)


## EAU
def water(x, y, o):
    pyxel.rect(x, y, 10, 10, 12)
    px, py = rot(2, 2, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(5, 6, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(8, 3, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(3, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(1, 8, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 1, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(7, 5, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(4, 4, o)
    pyxel.pset(x + px, y + py, 1)


def water_var1(x, y, o):
    pyxel.rect(x, y, 10, 10, 12)
    px, py = rot(2, 2, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(5, 6, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(8, 3, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(3, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(1, 8, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 1, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(7, 5, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(4, 4, o)
    pyxel.pset(x + px, y + py, 1)


def water_var2(x, y, o):
    pyxel.rect(x, y, 10, 10, 12)
    px, py = rot(3, 2, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 5, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(7, 2, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(2, 6, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(1, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(5, 1, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(8, 4, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(4, 3, o)
    pyxel.pset(x + px, y + py, 1)


def water_var3(x, y, o):
    pyxel.rect(x, y, 10, 10, 12)
    px, py = rot(1, 3, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(4, 7, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(9, 4, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(3, 6, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(2, 9, o)
    pyxel.pset(x + px, y + py, 5)
    px, py = rot(6, 2, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(7, 6, o)
    pyxel.pset(x + px, y + py, 1)
    px, py = rot(5, 5, o)
    pyxel.pset(x + px, y + py, 1)


## SABLE
def sand(x, y, o):
    pyxel.rect(x, y, 10, 10, 10)
    px, py = rot(2, 2, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(5, 6, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(8, 3, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(3, 7, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(1, 8, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(6, 1, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(7, 5, o)
    pyxel.pset(x + px, y + py, 9)
    px, py = rot(4, 4, o)
    pyxel.pset(x + px, y + py, 9)


## ARBRE
def tree(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 0, 163, 10, 10, 0)


def tree_2(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 11, 163, 10, 10, 0)


def tree_3(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 0, 174, 10, 10, 0)


def tree_4(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 11, 174, 10, 10, 0)


def tree_dirt(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 89, 0, 10, 10, 0)


def tree_dirt_2(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 67, 11, 10, 10, 0)


def tree_dirt_3(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 78, 11, 10, 10, 0)


def tree_dirt_4(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 89, 11, 10, 10, 0)


def apple_tree(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 22, 163, 10, 10, 0)


## MAISON
def house(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 32, 0, 10, 10, 0)


def broken_house(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 40, 0, 10, 10, 0)


def fishing_house(x, y):
    pyxel.rect(x, y, 10, 10, 10)
    pyxel.blt(x, y, 2, 100, 0, 10, 10, 0)


## PNG
def pnj1(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 0, 42, 10, 10, 0)


def pnj2(x, y):
    pyxel.rect(x, y, 10, 10, 10)
    pyxel.pset(x + 7, y + 5, 9)
    pyxel.pset(x + 6, y + 7, 9)
    pyxel.blt(x, y, 2, 0, 54, 10, 10, 0)


def pnj3(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 10, 42, 10, 10, 0)


def pnj4(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 10, 54, 10, 10, 0)


def pnj5(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 20, 42, 10, 10, 0)


def top_left_chief_house(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 33, 10, 10, 10, 0)


def top_right_chief_house(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 44, 10, 10, 10, 0)


def bottom_left_chief_house(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 33, 21, 10, 10, 0)


def bottom_right_chief_house(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 44, 21, 10, 10, 0)


## CHEMIN CLASSIQUE
def path_vertical(x, y):
    pyxel.blt(x, y, 2, 0, 240, 10, 10)


def path_horizontal(x, y):
    pyxel.blt(x, y, 2, 11, 240, 10, 10)


def path_corner_tl(x, y):
    pyxel.blt(x, y, 2, 33, 229, 10, 10)


def path_corner_tr(x, y):
    pyxel.blt(x, y, 2, 0, 229, 10, 10)


def path_corner_bl(x, y):
    pyxel.blt(x, y, 2, 11, 229, 10, 10)


def path_corner_br(x, y):
    pyxel.blt(x, y, 2, 22, 229, 10, 10)


def path_cross(x, y):
    pyxel.blt(x, y, 2, 0, 207, 10, 10)


def path_t_up(x, y):
    pyxel.blt(x, y, 2, 22, 218, 10, 10)


def path_t_down(x, y):
    pyxel.blt(x, y, 2, 0, 218, 10, 10)


def path_t_left(x, y):
    pyxel.blt(x, y, 2, 33, 218, 10, 10)


def path_t_right(x, y):
    pyxel.blt(x, y, 2, 11, 218, 10, 10)


    # RUINE
def ruin_hero(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 55, 0, 10, 10, 0)


def ruin_bulding(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 67, 0, 10, 10, 0)


def ruin_house(x, y):
    pyxel.rect(x, y, 10, 10, 9)
    pyxel.blt(x, y, 2, 78, 0, 10, 10, 0)


## TERRE
def dirt(x, y):
    pyxel.blt(x, y, 2, 56, 11, 10, 10)


def dirt_var1(x, y):
    pyxel.blt(x, y, 2, 56, 22, 10, 10)


def dirt_var2(x, y):
    pyxel.blt(x, y, 2, 67, 22, 10, 10)


def dirt_var3(x, y):
    pyxel.blt(x, y, 2, 78, 22, 10, 10)


## CHEMIN DE TERRE


def dirt_path_vertical(x, y):
    pyxel.blt(x, y, 2, 44, 240, 10, 10)


def dirt_path_horizontal(x, y):
    pyxel.blt(x, y, 2, 55, 240, 10, 10)


def dirt_path_corner_tl(x, y):
    pyxel.blt(x, y, 2, 77, 229, 10, 10)


def dirt_path_corner_tr(x, y):
    pyxel.blt(x, y, 2, 44, 229, 10, 10)


def dirt_path_corner_bl(x, y):
    pyxel.blt(x, y, 2, 55, 229, 10, 10)


def dirt_path_corner_br(x, y):
    pyxel.blt(x, y, 2, 66, 229, 10, 10)


def dirt_path_cross(x, y):
    pyxel.blt(x, y, 2, 44, 207, 10, 10)


def dirt_path_t_up(x, y):
    pyxel.blt(x, y, 2, 66, 218, 10, 10)


def dirt_path_t_down(x, y):
    pyxel.blt(x, y, 2, 44, 218, 10, 10)


def dirt_path_t_left(x, y):
    pyxel.blt(x, y, 2, 77, 218, 10, 10)


def dirt_path_t_right(x, y):
    pyxel.blt(x, y, 2, 55, 218, 10, 10)


##Mountain


def mountain(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 0, 196, 10, 10, 0)


def mountain_var1(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 11, 196, 10, 10, 0)


def mountain_var2(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 0, 185, 10, 10, 0)


def mountain_var3(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 11, 185, 10, 10, 0)


def wall_maze(x, y):
    pyxel.rect(x, y, 10, 10, 11)
    pyxel.blt(x, y, 2, 0, 142, 10, 10, 0)


##River
def river_vertical(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 88, 218, 10, 10, 0)


def river_horizontal(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 99, 218, 10, 10, 0)


def river_corner_br(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 110, 218, 10, 10, 0)


def river_corner_tl(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 121, 218, 10, 10, 0)


def river_corner_tr(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 132, 218, 10, 10, 0)


def river_corner_bl(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 143, 218, 10, 10, 0)


## Riviers sur sable


def sand_river_vertical(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 88, 229, 10, 10, 0)


def sand_river_horizontal(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 99, 229, 10, 10, 0)


def sand_river_corner_br(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 110, 229, 10, 10, 0)


def sand_river_corner_tl(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 121, 229, 10, 10, 0)


def sand_river_corner_tr(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 132, 229, 10, 10, 0)


def sand_river_corner_bl(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 143, 229, 10, 10, 0)


## Riviers sur terre


def earth_river_vertical(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 88, 240, 10, 10, 0)


def earth_river_horizontal(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 99, 240, 10, 10, 0)


def earth_river_corner_br(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 110, 240, 10, 10, 0)


def earth_river_corner_tl(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 121, 240, 10, 10, 0)


def earth_river_corner_tr(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 132, 240, 10, 10, 0)


def earth_river_corner_bl(x, y):
    pyxel.rect(x, y, 10, 10, 12)
    pyxel.blt(x, y, 2, 143, 240, 10, 10, 0)
