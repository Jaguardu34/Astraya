import pyxel
from world_map import tiles as t
from modules import variables as var

# 1-16 herbe avec variantes


#afficher la map
def print_map(nx, ny, taille, game_map, x, y):
  if taille % 2 != 0:
    for i in range(taille):
      for j in range(taille):

        map_x = int(x - (taille // 2) + j)
        map_y = int(y - (taille // 2) + i)

        def print_tile(color):
          pyxel.rect(nx + j * 10, ny + i * 10, 10, 10, color)

        if map_y < 0 or map_y >= len(game_map) or map_x < 0 or map_x >= len(
            game_map[map_y]):
          print_tile(5)
          continue

        tile = game_map[map_y][map_x]

        ## herbe et variante et rotations
        if tile in (1, 2, 3, 4):
          if tile == 1:
            t.herbe(nx + j * 10, ny + i * 10, 0)
          elif tile == 2:
            t.herbe(nx + j * 10, ny + i * 10, 1)
          elif tile == 3:
            t.herbe(nx + j * 10, ny + i * 10, 2)
          elif tile == 4:
            t.herbe(nx + j * 10, ny + i * 10, 3)
        elif tile in (5, 6, 7, 8):
          if tile == 5:
            t.herbe_var1(nx + j * 10, ny + i * 10, 0)
          elif tile == 6:
            t.herbe_var1(nx + j * 10, ny + i * 10, 1)
          elif tile == 7:
            t.herbe_var1(nx + j * 10, ny + i * 10, 2)
          elif tile == 8:
            t.herbe_var1(nx + j * 10, ny + i * 10, 3)
        elif tile in (9, 10, 11, 12):
          if tile == 9:
            t.herbe_var2(nx + j * 10, ny + i * 10, 0)
          elif tile == 10:
            t.herbe_var2(nx + j * 10, ny + i * 10, 1)
          elif tile == 11:
            t.herbe_var2(nx + j * 10, ny + i * 10, 2)
          elif tile == 12:
            t.herbe_var2(nx + j * 10, ny + i * 10, 3)
        elif tile in (13, 14, 15, 16):
          if tile == 13:
            t.herbe_var3(nx + j * 10, ny + i * 10, 0)
          elif tile == 14:
            t.herbe_var3(nx + j * 10, ny + i * 10, 1)
          elif tile == 15:
            t.herbe_var3(nx + j * 10, ny + i * 10, 2)
          elif tile == 16:
            t.herbe_var3(nx + j * 10, ny + i * 10, 3)

          ## eau
        elif tile in (101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                      112, 113, 114, 115, 116):
          if tile == 101:
            t.water(nx + j * 10, ny + i * 10, 0)
          elif tile == 102:
            t.water(nx + j * 10, ny + i * 10, 1)
          elif tile == 103:
            t.water(nx + j * 10, ny + i * 10, 2)
          elif tile == 104:
            t.water(nx + j * 10, ny + i * 10, 3)
          elif tile == 105:
            t.water_var1(nx + j * 10, ny + i * 10, 0)
          elif tile == 106:
            t.water_var1(nx + j * 10, ny + i * 10, 1)
          elif tile == 107:
            t.water_var1(nx + j * 10, ny + i * 10, 2)
          elif tile == 108:
            t.water_var1(nx + j * 10, ny + i * 10, 3)
          elif tile == 109:
            t.water_var2(nx + j * 10, ny + i * 10, 0)
          elif tile == 110:
            t.water_var2(nx + j * 10, ny + i * 10, 1)
          elif tile == 111:
            t.water_var2(nx + j * 10, ny + i * 10, 2)
          elif tile == 112:
            t.water_var2(nx + j * 10, ny + i * 10, 3)
          elif tile == 113:
            t.water_var3(nx + j * 10, ny + i * 10, 0)
          elif tile == 114:
            t.water_var3(nx + j * 10, ny + i * 10, 1)
          elif tile == 115:
            t.water_var3(nx + j * 10, ny + i * 10, 2)
          elif tile == 116:
            t.water_var3(nx + j * 10, ny + i * 10, 3)

          ## sable
        elif tile in (21, 22, 23, 24):
          if tile == 21:
            t.sand(nx + j * 10, ny + i * 10, 0)
          if tile == 22:
            t.sand(nx + j * 10, ny + i * 10, 1)
          if tile == 23:
            t.sand(nx + j * 10, ny + i * 10, 2)
          if tile == 24:
            t.sand(nx + j * 10, ny + i * 10, 3)

          ## arbre
        elif tile in (25, 74, 75, 76):
          if tile == 25:
            t.tree(nx + j * 10, ny + i * 10)
          elif tile == 74:
            t.tree_2(nx + j * 10, ny + i * 10)
          elif tile == 75:
            t.tree_3(nx + j * 10, ny + i * 10)
          elif tile == 76:
            t.tree_4(nx + j * 10, ny + i * 10)

          ## pnj
        elif tile in (26, 27, 28, 29, 30):
          if tile == 26:
            t.pnj1(nx + j * 10, ny + i * 10)
          elif tile == 27:
            t.pnj2(nx + j * 10, ny + i * 10)
          elif tile == 28:
            t.pnj3(nx + j * 10, ny + i * 10)
          elif tile == 29:
            t.pnj4(nx + j * 10, ny + i * 10)
          elif tile == 30:
            t.pnj5(nx + j * 10, ny + i * 10)

          ## maison
        elif tile == 31:
          t.house(nx + j * 10, ny + i * 10)
        elif tile == 32:
          t.broken_house(nx + j * 10, ny + i * 10)

          ## chemin
        elif tile in (33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43):
          if tile == 33:
            t.path_horizontal(nx + j * 10, ny + i * 10)
          elif tile == 34:
            t.path_vertical(nx + j * 10, ny + i * 10)
          elif tile == 35:
            t.path_corner_tl(nx + j * 10, ny + i * 10)
          elif tile == 36:
            t.path_corner_tr(nx + j * 10, ny + i * 10)
          elif tile == 37:
            t.path_corner_bl(nx + j * 10, ny + i * 10)
          elif tile == 38:
            t.path_corner_br(nx + j * 10, ny + i * 10)
          elif tile == 39:
            t.path_cross(nx + j * 10, ny + i * 10)
          elif tile == 40:
            t.path_t_up(nx + j * 10, ny + i * 10)
          elif tile == 41:
            t.path_t_down(nx + j * 10, ny + i * 10)
          elif tile == 42:
            t.path_t_left(nx + j * 10, ny + i * 10)
          elif tile == 43:
            t.path_t_right(nx + j * 10, ny + i * 10)

          ## maison du chef
        elif tile in (44, 45, 46, 47):
          if tile == 44:
            t.top_left_chief_house(nx + j * 10, ny + i * 10)
          elif tile == 45:
            t.top_right_chief_house(nx + j * 10, ny + i * 10)
          elif tile == 46:
            t.bottom_left_chief_house(nx + j * 10, ny + i * 10)
          elif tile == 47:
            t.bottom_right_chief_house(nx + j * 10, ny + i * 10)
          ## ruine
        elif tile == 48:
          t.ruin_hero(nx + j * 10, ny + i * 10)
        elif tile == 68:
          t.ruin_bulding(nx + j * 10, ny + i * 10)
        elif tile == 69:
          t.ruin_house(nx + j * 10, ny + i * 10)

        ## arbre sur terre
        elif tile in (49, 50, 51, 52):
          if tile == 49:
            t.tree_dirt(nx + j * 10, ny + i * 10)
          elif tile == 50:
            t.tree_dirt_2(nx + j * 10, ny + i * 10)
          elif tile == 51:
            t.tree_dirt_3(nx + j * 10, ny + i * 10)
          elif tile == 52:
            t.tree_dirt_4(nx + j * 10, ny + i * 10)

          ## terre
        elif tile in (53, 54, 55, 56):
          if tile == 53:
            t.dirt(nx + j * 10, ny + i * 10)
          elif tile == 54:
            t.dirt_var1(nx + j * 10, ny + i * 10)
          elif tile == 55:
            t.dirt_var2(nx + j * 10, ny + i * 10)
          elif tile == 56:
            t.dirt_var3(nx + j * 10, ny + i * 10)
        elif tile in (57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67):
          if tile == 57:
            t.dirt_path_horizontal(nx + j * 10, ny + i * 10)
          elif tile == 58:
            t.dirt_path_vertical(nx + j * 10, ny + i * 10)
          elif tile == 59:
            t.dirt_path_corner_tl(nx + j * 10, ny + i * 10)
          elif tile == 60:
            t.dirt_path_corner_tr(nx + j * 10, ny + i * 10)
          elif tile == 61:
            t.dirt_path_corner_bl(nx + j * 10, ny + i * 10)
          elif tile == 62:
            t.dirt_path_corner_br(nx + j * 10, ny + i * 10)
          elif tile == 63:
            t.dirt_path_cross(nx + j * 10, ny + i * 10)
          elif tile == 64:
            t.dirt_path_t_up(nx + j * 10, ny + i * 10)
          elif tile == 65:
            t.dirt_path_t_down(nx + j * 10, ny + i * 10)
          elif tile == 66:
            t.dirt_path_t_left(nx + j * 10, ny + i * 10)
          elif tile == 67:
            t.dirt_path_t_right(nx + j * 10, ny + i * 10)

        ## montagne
        elif tile in (70, 71, 72, 73):
          if tile == 70:
            t.mountain(nx + j * 10, ny + i * 10)
          elif tile == 71:
            t.mountain_var1(nx + j * 10, ny + i * 10)
          elif tile == 72:
            t.mountain_var2(nx + j * 10, ny + i * 10)
          elif tile == 73:
            t.mountain_var3(nx + j * 10, ny + i * 10)

        ## mur du labyrinthe
        elif tile == 77:
          t.wall_maze(nx + j * 10, ny + i * 10)

        ## riviers ( pas utilisé )
        elif tile in (78, 79, 80, 81, 82, 83):
          if tile == 78:
            t.river_vertical(nx + j * 10, ny + i * 10)
          elif tile == 79:
            t.river_horizontal(nx + j * 10, ny + i * 10)
          elif tile == 80:
            t.river_corner_br(nx + j * 10, ny + i * 10)
          elif tile == 81:
            t.river_corner_tl(nx + j * 10, ny + i * 10)
          elif tile == 82:
            t.river_corner_tr(nx + j * 10, ny + i * 10)
          elif tile == 83:
            t.river_corner_bl(nx + j * 10, ny + i * 10)

        elif tile in (84, 85, 86, 87, 88, 89):
          if tile == 84:
            t.sand_river_vertical(nx + j * 10, ny + i * 10)
          elif tile == 85:
            t.sand_river_horizontal(nx + j * 10, ny + i * 10)
          elif tile == 86:
            t.sand_river_corner_br(nx + j * 10, ny + i * 10)
          elif tile == 87:
            t.sand_river_corner_tl(nx + j * 10, ny + i * 10)
          elif tile == 88:
            t.sand_river_corner_tr(nx + j * 10, ny + i * 10)
          elif tile == 89:
            t.sand_river_corner_bl(nx + j * 10, ny + i * 10)

        elif tile in (90, 91, 92, 93, 94, 95):
          if tile == 90:
            t.earth_river_vertical(nx + j * 10, ny + i * 10)
          elif tile == 91:
            t.earth_river_horizontal(nx + j * 10, ny + i * 10)
          elif tile == 92:
            t.earth_river_corner_br(nx + j * 10, ny + i * 10)
          elif tile == 93:
            t.earth_river_corner_tl(nx + j * 10, ny + i * 10)
          elif tile == 94:
            t.earth_river_corner_tr(nx + j * 10, ny + i * 10)
          elif tile == 95:
            t.earth_river_corner_bl(nx + j * 10, ny + i * 10)
        elif tile == 96:
          t.fishing_house(nx + j * 10, ny + i * 10)
        elif tile == 98:
          t.apple_tree(nx + j * 10, ny + i * 10)
        else:
          print_tile(0)
    #coord left=1 right=2 face=3 back=4
    coord = {
        "right": (0, 0),
        "right2": (10, 0),
        "left": (0, 10),
        "left2": (10, 10),
        "face": (0, 30),
        "face2": (10, 30),
        "back": (0, 20),
        "back2": (10, 20)
    }
    #afficher animation joueur
    if var.player_animation_timer <= 0:
      var.player_animation_timer = 30
    if var.orientation == "right":
      if var.player_animation_timer > 15:
        u, v = coord["right"]
      else:
        u, v = coord["right2"]
    elif var.orientation == "left":
      if var.player_animation_timer > 15:
        u, v = coord["left"]
      else:
        u, v = coord["left2"]
    elif var.orientation == "face":
      if var.player_animation_timer > 15:
        u, v = coord["face"]
      else:
        u, v = coord["face2"]
    elif var.orientation == "back":
      if var.player_animation_timer > 15:
        u, v = coord["back"]
      else:
        u, v = coord["back2"]
    pyxel.blt(nx + (taille * 10) / 2 - 5, ny + (taille * 10) / 2 - 5, 2, u, v,
              10, 10, 0)
    pyxel.text(nx, ny, f"Map x:{x} y:{y}", 4)
    taille_minimap = 40
    #afficher la minimap en bas a droite
    print_minimap((nx + taille * 10) - taille_minimap - 2,
                  (ny + taille * 10) - taille_minimap - 2, taille_minimap,
                  game_map, x, y)
  else:
    print("La taille de la map doit etre impaire")


#afficher la minimap
def print_minimap(nx, ny, taille, game_map, x, y):
  pyxel.rect(nx, ny, taille + 2, taille + 2, 10)
  for i in range(taille):
    for j in range(taille):
      map_x = int(x - (taille / 2) + j)
      map_y = int(y - (taille / 2) + i)

      def print_tile(color):
        pyxel.rect(nx + 1 + j * 1, ny + 1 + i * 1, 1, 1, color)

      if map_y < 0 or map_y >= len(game_map) or map_x < 0 or map_x >= len(
          game_map[map_y]):
        print_tile(5)
        continue

      tile = game_map[map_y][map_x]

      if tile in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 57,
                  58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 77, 98):
        print_tile(11)
      elif tile in (17, 18, 19, 20, 101, 102, 103, 104, 105, 106, 107, 108,
                    109, 110, 111, 112, 113, 114, 115, 116):
        print_tile(5)
      elif tile in (21, 22, 23, 24):
        print_tile(10)
      elif tile in (25, 49, 50, 51, 52, 74, 75, 76):
        print_tile(3)
      elif tile in (26, 27, 28, 29, 30):
        print_tile(15)
      elif tile in (31, 32, 44, 45, 46, 47, 53, 54, 55, 56,96):
        print_tile(9)
      elif tile in (33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 48, 68, 69, 70,
                    71, 72, 73):
        print_tile(13)
      else:
        print_tile(0)
  pyxel.rect(nx + 1 + taille / 2, ny + 1 + taille / 2, 1, 1, 0)
  pyxel.text(nx + 1, ny + 1, "Minimap", 0)
