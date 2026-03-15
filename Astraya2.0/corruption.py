import random
from settings import *

def generer_corruption(biome_map, nb_zones=5):

    taille_min = 8000
    taille_max = 15000

    # Biomes qui peuvent être corrompus
    corruptibles = {
        BIOME_IDS["plains"],
        BIOME_IDS["forest"],
        BIOME_IDS["jungle"],
        BIOME_IDS["mountains"]
    }
    centres = [(1400, 1400)]
    for i in range(nb_zones):
        attempts = 0
        taille_zone = random.randint(taille_min, taille_max)
        
        while attempts < 1000:
            centre_x = random.randint(50, SIZE - 50)
            centre_y = random.randint(50, SIZE - 50)
            centres.append((centre_x, centre_y))

            centre_x = centres[i][0]
            centre_y = centres[i][1]
                

            if biome_map[centre_y][centre_x] not in corruptibles:
                attempts += 1
                centres.remove((centre_x, centre_y))
                continue

            corrompus = [(centre_x, centre_y)]
            a_traiter = [(centre_x, centre_y)] # pts à traiter pour expansion

            while len(corrompus) < taille_zone and a_traiter:
                # On prend un point aléatoire dans la liste
                idx = random.randint(0, len(a_traiter) - 1)
                current_x, current_y = a_traiter.pop(idx)

                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(directions)

                for dx, dy in directions:
                    new_x = current_x + dx
                    new_y = current_y + dy

                    if 0 <= new_x < SIZE and 0 <= new_y < SIZE and (new_x, new_y) not in corrompus:
                        random_chance = random.random()
                        if biome_map[new_y, new_x] in corruptibles: 
                            corrompus.append((new_x, new_y))
                            a_traiter.append((new_x, new_y))

            for x, y in corrompus:
                biome_map[y, x] = BIOME_IDS["corrupted"]

            
            if len(corrompus) >= taille_zone * 0.5:  
                break
            
            attempts += 1
                
    return biome_map
