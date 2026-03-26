import random
import pygame
import numpy as np
from settings import *
from classes import entity

def generer_corruption(biome_map, nb_zones=5):
    taille_min = 8000
    taille_max = 15000
    f_origin_donjon_coords = []
    maps_donjon = []
    corruptibles = {
        BIOME_IDS["plains"],
        BIOME_IDS["forest"],
        BIOME_IDS["jungle"],
        BIOME_IDS["mountains"]
    }

    def corrompre_zone(biome_map, centre_x, centre_y, taille_zone):
        """Corrompt une zone autour d'un centre donné."""
        corrompus = set()
        corrompus.add((centre_x, centre_y))
        a_traiter = [(centre_x, centre_y)]

        while len(corrompus) < taille_zone and a_traiter:
            idx = random.randint(0, len(a_traiter) - 1)
            current_x, current_y = a_traiter.pop(idx)

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                new_x = current_x + dx
                new_y = current_y + dy
                if (0 <= new_x < SIZE and 0 <= new_y < SIZE
                        and (new_x, new_y) not in corrompus
                        and biome_map[new_y, new_x] in corruptibles):
                    corrompus.add((new_x, new_y))
                    a_traiter.append((new_x, new_y))

        for x, y in corrompus:
            biome_map[y, x] = BIOME_IDS["corrupted"]

        donjon_coords = create_donjon_coords(centre_x, centre_y, taille=15)
        f_origin_donjon_coords.append((centre_x, centre_y))
        for x, y in donjon_coords:
            biome_map[y, x] = BIOME_IDS["donjon_collide"]

        return f_origin_donjon_coords

   
    taille_fixe = random.randint(taille_min, taille_max)
    f_origin_donjon_coords = corrompre_zone(biome_map, 1400, 1400, taille_fixe)


    for _ in range(nb_zones):
        taille_zone = random.randint(taille_min, taille_max)
        attempts = 0

        while attempts < 10000:
            centre_x = random.randint(50, SIZE - 50)
            centre_y = random.randint(50, SIZE - 50)

            if biome_map[centre_y][centre_x] not in corruptibles:
                attempts += 1
                continue


            f_origin_donjon_coords = corrompre_zone(biome_map, centre_x, centre_y, taille_zone)
            break

    maps_donjon.append(create_inside_donjon_map())
    return biome_map, f_origin_donjon_coords, maps_donjon


def create_donjon_coords(center_x, center_y, taille):
    
    if taille % 2 == 0:
        taille += 1

    rayon = taille // 2
    donjon_coords = []

    for y in range(center_y - rayon, center_y + rayon + 1):
        for x in range(center_x - rayon, center_x + rayon + 1):
            donjon_coords.append((x, y))

    return donjon_coords


# TODO mettre les textures + 
def create_inside_donjon_map(): # Peut etre ajouter type de donjon en parametre

    dungeon_size = 50
    dungeon_map = np.full((dungeon_size, dungeon_size), BIOME_IDS["donjon_collide"], dtype=np.uint32)

    for y in range(1, dungeon_size - 1):
        for x in range(1, dungeon_size - 1):
            dungeon_map[y, x] = BIOME_IDS["plains"]


    return dungeon_map


def spawn_dungeon_doors(origin_donjon_coords, world_map, altitude_map, entity_grp):

    door_surface = pygame.Surface((32, 32))
    door_surface.fill((150, 75, 0))  # marron

    for dungeon_index, (cx, cy) in enumerate(origin_donjon_coords):

        # --- Le donjon fait 15x15 dans ton code ---
        taille = 15
        rayon = taille // 2

        # Coordonnées du bas du donjon
        bottom_y = cy + rayon
        bottom_x = cx  # centré

        # Sécurité : éviter de sortir de la map
        if 0 <= bottom_x < world_map.shape[1] and 0 <= bottom_y < world_map.shape[0]:

            # On place la porte sur la map surface
            world_map[bottom_y, bottom_x] = BIOME_IDS["donjon_collide"]

            # Création de la porte
            door = entity.DungeonDoor(
                [door_surface],
                world_map,
                altitude_map,
                x=bottom_x,
                y=bottom_y
            )

            door.dungeon_index = dungeon_index
            door.is_exit = False  # entrée
            entity_grp.add(door)

            print(f" Porte de donjon #{dungeon_index} placée en ({bottom_x}, {bottom_y})")

        else:
            print(f"Impossible de placer la porte du donjon #{dungeon_index} (hors map)")
