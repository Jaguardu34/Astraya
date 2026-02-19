import random

size = 80
center_x = 40
center_y = 40
dirt_center_x = 50
dirt_center_y = 50
radius_big = 32
radius_small = 29

ellipse_center_x = 25
ellipse_center_y = 32

ellipse_radius_x = 12
ellipse_radius_y = 6


#map
def create_map(largeur, hauteur):
    game_map = []
    for y in range(hauteur):
        ligne = []
        for x in range(largeur):

            ## Aide de chatgpt pour la génération de la map ronde
            distance_sq = (y - center_y)**2 + (
                x - center_x
            )**2  ## Calcule de la distance au carré entre le centre et le point actuel

            # Île principale (herbe)
            if distance_sq <= radius_small**2:  ## Si cette distance est inférieure ou égale a 29² alors on pose de l'herbe
                val = random.randint(11, 16)

            # Bande de sable autour de l'île
            elif distance_sq <= radius_big**2:  ## Sinon si la distance est inférieure ou égale a 32² alors on pose du sable
                val = random.randint(21, 23)

            # Eau autour
            else:
                val = random.randint(101, 116)  ## Sinon on pose de l'eau

            distance_sq_dirt = (y - dirt_center_y)**2 + (x - dirt_center_x)**2

            if distance_sq_dirt <= 14**2:  ## montagne
                val = random.randint(70, 73)

            if distance_sq_dirt <= 13**2:  ## arbre
                val = random.choice([25, 74, 75, 76])

            if distance_sq_dirt <= 12**2:  ## arbre sur terre
                val = random.randint(49, 52)

            if distance_sq_dirt <= 11**2:  ## terre
                val = random.randint(53, 56)

            if ((x - ellipse_center_x)**2 / ellipse_radius_x**2 +
                (y - ellipse_center_y)**2 / ellipse_radius_y**2) <= 1:
                val = random.choice([25, 74, 75, 76])

            ligne.append(val)
        game_map.append(ligne)

    ## Eléments spécifique a position spécifique

    #Village principal

    ## Route
    game_map[40][20] = 39
    game_map[40][21] = 33
    game_map[40][22] = 33
    game_map[40][23] = 33
    game_map[40][24] = 33
    game_map[40][25] = 42
    game_map[41][25] = 34
    game_map[42][25] = 34
    game_map[39][25] = 34
    game_map[38][25] = 42
    game_map[38][24] = 33
    game_map[37][25] = 34
    game_map[39][20] = 34
    game_map[38][20] = 35
    game_map[38][19] = 33
    game_map[37][19] = 31
    game_map[33][25] = 36
    game_map[33][31] = 37
    game_map[32][31] = 34
    game_map[31][31] = 34
    for i in range(3):
        game_map[34 + i][25] = 34
    for i in range(5):
        game_map[33][26 + i] = 33

    ## Maison
    game_map[39][26] = 31
    game_map[41][24] = 31
    game_map[39][21] = 31
    game_map[37][24] = 32

    game_map[39][15] = 44
    game_map[40][15] = 46
    game_map[39][16] = 45
    game_map[40][16] = 47

    game_map[63][17] = 96
    ## PNG
    game_map[36][24] = 26
    game_map[40][17] = 30
    game_map[63][18] = 27

    ## Arbre
    game_map[56][20] = 98
    game_map[49][21] = 98
    game_map[43][20] = 98
    game_map[60][19] = 98
    ## route en ruine
    game_map[50][50] = 63
    game_map[50][51] = 57
    game_map[50][52] = 57
    game_map[50][53] = 61
    game_map[49][53] = 58
    game_map[48][53] = 58
    game_map[51][50] = 58
    game_map[50][49] = 57
    game_map[50][48] = 57
    game_map[49][50] = 58
    game_map[48][50] = 65
    game_map[48][51] = 57
    game_map[50][47] = 67
    ##ruine
    game_map[49][54] = 68
    game_map[51][51] = 69
    game_map[48][49] = 69
    game_map[47][51] = 68
    game_map[50][46] = 48
    ## riviere

    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j] == random.randint(1, 16):
                game_map[i][j] = random.choice([25, 74, 75, 76])

    return game_map
