import numpy as np
import random
import matplotlib.pyplot as plt
import pickle
import os
from settings import *
from classes.village import *
from falaises import *

def map_generate():
    
    # ==============================================================================
    # CONFIGURATION
    # ==============================================================================
    SIZE = 2000
    NB_VILLAGES = 80

    ID_TO_BIOME = {v: k for k, v in BIOME_IDS.items()}

    # ==============================================================================
    # GÉNÉRATION DE BRUIT PERLIN
    # ==============================================================================

    def perlin(width, height, scale=10, seed=SEED):
        """Génère un bruit de Perlin vectorisé."""
        rng = np.random.default_rng(seed)

        gx = rng.uniform(-1, 1, (width//scale + 2, height//scale + 2))
        gy = rng.uniform(-1, 1, (width//scale + 2, height//scale + 2))

        x = np.linspace(0, width/scale, width)
        y = np.linspace(0, height/scale, height)
        xx, yy = np.meshgrid(x, y)

        x0 = xx.astype(int)
        y0 = yy.astype(int)
        xf = xx - x0
        yf = yy - y0

        g00 = gx[x0,     y0    ] * xf     + gy[x0,     y0    ] * yf
        g10 = gx[x0 + 1, y0    ] * (xf-1) + gy[x0 + 1, y0    ] * yf
        g01 = gx[x0,     y0 + 1] * xf     + gy[x0,     y0 + 1] * (yf-1)
        g11 = gx[x0 + 1, y0 + 1] * (xf-1) + gy[x0 + 1, y0 + 1] * (yf-1)

        u = xf * xf * (3 - 2 * xf)
        v = yf * yf * (3 - 2 * yf)

        return (1 - u) * ((1 - v) * g00 + v * g01) + u * ((1 - v) * g10 + v * g11)


    def fractal_noise(scale, seed):
        """Génère un bruit fractal multi-octaves."""
        base = perlin(SIZE, SIZE, scale=scale, seed=seed)
        mid  = perlin(SIZE, SIZE, scale=scale//2, seed=seed+1) * 0.5
        fine = perlin(SIZE, SIZE, scale=scale//4, seed=seed+2) * 0.25
        return base + mid + fine


    def norm(a):
        """Normalise un array entre 0 et 1."""
        return (a - a.min()) / (a.max() - a.min())


    # ==============================================================================
    # MASQUE D'ÎLE
    # ==============================================================================

    def create_island_mask(size, falloff=0.4):
        """Crée un masque radial pour forcer les bords à être de l'océan."""
        y, x = np.ogrid[0:size, 0:size]
        center = size / 2
        
        dx = (x - center) / center
        dy = (y - center) / center
        distance = np.sqrt(dx**2 + dy**2)
        
        mask = np.clip(1 - (distance - (1 - falloff)) / falloff, 0, 1)
        
        return mask


    # ==============================================================================
    # MONDE DE SURFACE
    # ==============================================================================

    def generate_overworld():
        """Génère les cartes de hauteur, humidité et température avec masque d'île."""
        heightmap = fractal_noise(scale=300, seed=1)
        altitude_map = np.zeros((SIZE, SIZE), dtype=np.int8) # On a des niveaux d'altitude
        humiditymap = fractal_noise(scale=500, seed=2)
        temperaturemap = fractal_noise(scale=500, seed=3)
        
        island_mask = create_island_mask(SIZE, falloff=0.4)
        
        heightmap = norm(heightmap)
        heightmap = heightmap * island_mask

        altitude_map[heightmap < 0.40] = 0  # Plaines
        altitude_map[(heightmap >= 0.40) & (heightmap < 0.58)] = 2  # Niveau 1 
        altitude_map[(heightmap >= 0.58) & (heightmap < 0.70)] = 4  # Niveau 2 (plaines, jungle, forêt selon humidité/température)
        altitude_map[(heightmap >= 0.70) & (heightmap < 0.85)] = 6  # Montagnes
        altitude_map[heightmap >= 0.85] = 8  # Pics enneigés
        
        return heightmap, norm(humiditymap), norm(temperaturemap), altitude_map  

    def poser_falaises(biome_map, nb_falaises=100):

        autorises = {
        BIOME_IDS["plains"],
        BIOME_IDS["forest"],
        BIOME_IDS["jungle"],
        BIOME_IDS["mountains"],
        BIOME_IDS["beach"]
    }
        
        for _ in range(nb_falaises):
            attempts = 0
            trouve = False
            while attempts < 10000 and not trouve:
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)

                falaises = create_falaise(x, y)

                valide = True
                for xx, yy in falaises:
                    if biome_map[yy][xx] not in autorises:
                        valide = False
                        break

                if valide:
                    coins = []
                    for i in range(1, len(falaises) - 1):
                        x1, y1 = falaises[i][0], falaises[i][1]

                        if (x1 + 1, y1) in falaises and (x1, y1 + 1) in falaises:
                            coins.append((x1, y1))
                        if (x1 + 1, y1) in falaises and (x1, y1 - 1) in falaises:
                            coins.append((x1, y1))
                        if (x1 - 1, y1) in falaises and (x1, y1 + 1) in falaises:
                            coins.append((x1, y1))
                        if (x1 - 1, y1) in falaises and (x1, y1 - 1) in falaises:
                            coins.append((x1, y1))

                    pos_deb = random.randint(0, len(coins) - 1)
                    falaises = falaises[pos_deb:] + falaises[:pos_deb]

                    for i in range(len(falaises)): 
                        current_x, current_y = falaises[i][0], falaises[i][1]
                        currrnt_orientation = "N"
                        if (current_x - 1, current_y) in falaises and (current_x + 1, current_y) in falaises :
                            biome_map[current_y, current_x] = BIOME_IDS["cliff_" + currrnt_orientation]
                            current_x += 1

                        elif (current_x, current_y - 1) in falaises and (current_x, current_y + 1) in falaises :
                            biome_map[current_y, current_x] = BIOME_IDS["cliff_" + currrnt_orientation]
                            current_y += 1

                        elif (current_x + 1, current_y) in falaises and (current_x, current_y + 1) in falaises :
                            biome_map[current_y, current_x] = BIOME_IDS["cliff_NE"]
                            current_x -= 1
                            current_y -= 1
                            if currrnt_orientation == "N":
                                currrnt_orientation = "E"
                            if currrnt_orientation == "E":
                                currrnt_orientation = "N"
                        
                        elif (current_x - 1, current_y) in falaises and (current_x, current_y + 1) in falaises :
                            biome_map[current_y, current_x] = BIOME_IDS["cliff_NO"]
                            current_x += 1
                            current_y -= 1
                            if currrnt_orientation == "N":
                                currrnt_orientation = "O"
                            if currrnt_orientation == "O":
                                currrnt_orientation = "N"

                        elif (current_x + 1, current_y) in falaises and (current_x, current_y - 1) in falaises :
                            biome_map[current_y, current_x] = BIOME_IDS["cliff_SE"]
                            current_x -= 1
                            current_y += 1
                            if currrnt_orientation == "S":
                                currrnt_orientation = "E"
                            if currrnt_orientation == "E":
                                currrnt_orientation = "S"

                        elif (current_x - 1, current_y) in falaises and (current_x, current_y - 1) in falaises :
                            biome_map[current_y, current_x] = BIOME_IDS["cliff_SO"]
                            current_x += 1
                            current_y += 1
                            if currrnt_orientation == "S":
                                currrnt_orientation = "O"
                            if currrnt_orientation == "O":
                                currrnt_orientation = "S"

                        # gauche a droite
                        elif (current_x - 1, current_y) in falaises and (current_x + 1, current_y) not in falaises and (current_x, current_y - 1) not in falaises and (current_x, current_y + 1) not in falaises:
                            biome_map[current_y, current_x] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_1"]
                            biome_map[current_y, current_x + 2] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_2"]
                            biome_map[current_y, current_x + 3] = BIOME_IDS["cliff_" + currrnt_orientation]
                            current_x += 3

                        # gauche a droite
                        elif (current_x + 1, current_y) in falaises and (current_x - 1, current_y) not in falaises and (current_x, current_y - 1) not in falaises and (current_x, current_y + 1) not in falaises:
                            biome_map[current_y, current_x] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_1"]
                            biome_map[current_y, current_x - 2] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_2"]
                            biome_map[current_y, current_x - 3] = BIOME_IDS["cliff_" + currrnt_orientation]
                            current_x -= 3
                        
                        # bas en haut
                        elif (current_x, current_y - 1) in falaises and (current_x, current_y + 1) not in falaises and (current_x - 1, current_y) not in falaises and (current_x + 1, current_y + 1) not in falaises:
                            biome_map[current_y, current_x] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_1"]
                            biome_map[current_y + 2, current_x ] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_2"]
                            biome_map[current_y + 3, current_x ] = BIOME_IDS["cliff_" + currrnt_orientation]
                            current_y += 3

                        # haut en bas
                        elif (current_x, current_y + 1) in falaises and (current_x, current_y - 1) not in falaises and (current_x - 1, current_y) not in falaises and (current_x + 1, current_y) not in falaises:
                            biome_map[current_y, current_x] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_1"]
                            biome_map[current_y - 2, current_x ] = BIOME_IDS["passage_cliff_" + currrnt_orientation + "_2"]
                            biome_map[current_y - 3, current_x ] = BIOME_IDS["cliff_" + currrnt_orientation]
                            current_y -= 3             
                    trouve = True

        return biome_map


    def compute_biomes_vectorized(heightmap, humiditymap, temperaturemap):
        """Calcule les biomes avec NumPy"""
        biomes = np.zeros((SIZE, SIZE), dtype=np.uint32)
        
        # Masques booléens pour chaque biome
        ocean_mask = heightmap < 0.25
        beach_mask = (heightmap >= 0.25) & (heightmap < 0.32)
        
        jungle_mask = (heightmap >= 0.32) & (heightmap < 0.65) & (humiditymap > 0.6) & (temperaturemap > 0.5)
        forest_mask = (heightmap >= 0.32) & (heightmap < 0.65) & (humiditymap > 0.4) & (temperaturemap > 0.3) & ~jungle_mask
        plains_mask = (heightmap >= 0.32) & (heightmap < 0.65) & ~jungle_mask & ~forest_mask
        
        mountains_mask = (heightmap >= 0.65) & (heightmap < 0.80)
        snow_mask = heightmap >= 0.80
        
        # Attribution en une seule opération vectorisée
        biomes[ocean_mask] = BIOME_IDS["ocean"]
        biomes[beach_mask] = BIOME_IDS["beach"]
        biomes[plains_mask] = BIOME_IDS["plains"]
        biomes[jungle_mask] = BIOME_IDS["jungle"]
        biomes[forest_mask] = BIOME_IDS["forest"]
        biomes[mountains_mask] = BIOME_IDS["mountains"]
        biomes[snow_mask] = BIOME_IDS["snow_peak"]

        biomes = poser_falaises(biomes, nb_falaises=100)
        
        return biomes


    # ==============================================================================
    # GROTTES
    # ==============================================================================

    def generate_cave_system():
        """Génère le système de grottes avec NumPy."""
        cave_noise = (
            perlin(SIZE, SIZE, scale=80, seed=100) * 0.6 +
            perlin(SIZE, SIZE, scale=40, seed=101) * 0.3 +
            perlin(SIZE, SIZE, scale=20, seed=102) * 0.1
        )
        cave_noise = norm(cave_noise)

        # Carte air/roche (vectorisée)
        cave_map = np.where(cave_noise < 0.50, BIOME_IDS["air"], BIOME_IDS["rock"])

        biome_noise = (
            perlin(SIZE, SIZE, scale=120, seed=300) * 0.6 +
            perlin(SIZE, SIZE, scale=60, seed=301) * 0.3 +
            perlin(SIZE, SIZE, scale=30, seed=302) * 0.1
        )
        biome_noise = norm(biome_noise)

        # Cave biomes (vectorisé)
        cave_biomes = np.copy(cave_map)
        
        # Masque pour les zones d'air uniquement
        air_mask = cave_map == BIOME_IDS["air"]
        
        # Attribution des biomes souterrains (vectorisé)
        cave_biomes[air_mask & (biome_noise < 0.20)] = BIOME_IDS["cave_ice"]
        cave_biomes[air_mask & (biome_noise >= 0.20) & (biome_noise < 0.40)] = BIOME_IDS["cave_mushroom"]
        cave_biomes[air_mask & (biome_noise >= 0.40) & (biome_noise < 0.60)] = BIOME_IDS["cave_normal"]
        cave_biomes[air_mask & (biome_noise >= 0.60) & (biome_noise < 0.80)] = BIOME_IDS["cave_crystal"]
        cave_biomes[air_mask & (biome_noise >= 0.80)] = BIOME_IDS["cave_lava"]

        return cave_map, cave_noise, cave_biomes, biome_noise


    # ==============================================================================
    # VILLAGES
    # ==============================================================================

    def generate_villages(biome_map, nb_villages=NB_VILLAGES):
        """Place des villages en évitant l'océan."""
        coord_vil = []
        ocean_id = BIOME_IDS["ocean"]

        for _ in range(nb_villages):
            attempts = 0
            trouve = False
            while attempts < 10000 and not trouve:
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)
                
                if biome_map[y][x] != ocean_id:
                    coord_vil.append([x, y])
                    trouve = True
                attempts += 1

        return coord_vil

    def classify_villages(coord_vil, biome_map, nb_villes=3, rayon_proximite=1000):
        """Classe les villages en 3 grandes villes, 10 grands villages, le reste villages."""

        # 1. Calcul de la densité locale pour chaque village
        densites = []
        for i, (vx, vy) in enumerate(coord_vil):
            densite = sum(
                1 for ox, oy in coord_vil
                if (ox - vx)**2 + (oy - vy)**2 < rayon_proximite**2
            )
            densites.append((densite, vx, vy))

        # 2. On trie par densité croissante (les plus isolés d'abord)
        densites.sort(key=lambda x: x[0])

        candidats = densites[:20]

        villes = []

        # On choisit la première ville : la plus isolée
        _, vx0, vy0 = candidats[0]
        villes.append((vx0, vy0))

        # Sélection des autres villes
        while len(villes) < nb_villes:
            meilleur = None
            meilleure_dist = -1

            for _, vx, vy in candidats:
                # distance minimale à une ville déjà choisie
                dist_min = min(
                    (vx - cx)**2 + (vy - cy)**2
                    for cx, cy in villes
                )

                if dist_min > meilleure_dist:
                    meilleure_dist = dist_min
                    meilleur = (vx, vy)

            villes.append(meilleur)
        villes.append((1500, 1600))  # Ajouter la ville centrale

        # 5. Création des objets Village
        resultat = []
        for vx, vy in villes:
            biome = biome_map[vy, vx]
            resultat.append(Village(vx, vy, "city", biome))

        return resultat


    



            




    # ==============================================================================
    # GROTTES (ENTRÉES)
    # ==============================================================================

    def generate_grottes(biome_map, nb_grottes=NB_VILLAGES):
        """Place des entrées de grottes en évitant l'océan."""
        coord_grottes = [[1500, 1501]]
        ocean_id = BIOME_IDS["ocean"]

        for _ in range(nb_grottes):
            attempts = 0
            trouve = False
            while attempts < 10000 and not trouve:
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)
                
                if biome_map[y][x] != ocean_id:
                    coord_grottes.append([x, y])
                    trouve = True
                attempts += 1

        return coord_grottes


    # ==============================================================================
    # VARIATIONS DE TEXTURES
    # ==============================================================================

    def add_texture_variants(biome_map):
        """Ajoute des variations de textures pour beach et plains."""
        # Créer un array de variations (0-255 pour chaque tile) avnt c'était 16 mais c'est trop borring
        texture_variants = np.random.randint(0, 255, size=(SIZE, SIZE), dtype=np.uint32)

        # Retourner les deux arrays séparément
        return biome_map, texture_variants


    # ==============================================================================
    # SAUVEGARDE / CHARGEMENT
    # ==============================================================================

    def save_world(filename, biome_map, texture_variants, cave_biomes, coord_vil, coord_grottes, altitude_map):
        """Sauvegarde le monde généré."""
        data = {
            'biome_map': biome_map,
            'texture_variants': texture_variants,
            'cave_biomes': cave_biomes,
            'coord_vil': coord_vil,
            'coord_grottes': coord_grottes,
            'altitude_map': altitude_map, 
            'size': SIZE
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"✅ Monde sauvegardé : {filename}")


    def load_world(filename):
        """Charge un monde sauvegardé."""
        if not os.path.exists(filename):
            return None
        
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        
        print(f" Monde chargé depuis : {filename}")
        return (data['biome_map'], data['texture_variants'], data['cave_biomes'], 
                data['coord_vil'], data['coord_grottes'], data.get('altitude_map'))


    # ==============================================================================
    # RENDU (pour visualisation)
    # ==============================================================================

    def render_overworld_map(biome_map, village_coords=None, grottes_coords=None):
        """Génère l'image de surface."""
        colors = {
            0: [0.0, 0.3, 1.0],    # ocean
            1: [1.0, 0.9, 0.6],    # beach
            2: [0.5, 0.8, 0.2],    # plains
            3: [0.1, 0.5, 0.1],    # jungle
            4: [0.05, 0.3, 0.05],  # forest
            5: [0.5, 0.5, 0.5],    # mountains
            6: [1.0, 1.0, 1.0],    # snow_peak
            7: [1.0, 0.0, 1.0],    # collide
        }

        img = np.zeros((SIZE, SIZE, 3))
        for biome_id, color in colors.items():
            mask = biome_map == biome_id
            img[mask] = color

        if village_coords:
            for x, y in village_coords:
                if 0 <= y < SIZE and 0 <= x < SIZE:
                    img[y, x] = [1.0, 0.0, 0.0]  # Rouge

        if grottes_coords:
            for x, y in grottes_coords:
                if 0 <= y < SIZE and 0 <= x < SIZE:
                    img[y, x] = [0.6, 1.0, 1.0]  # Cyan

        return img


    def render_cave_map(cave_biomes):
        """Génère l'image souterraine."""
        colors = {
            10: [0.1, 0.1, 0.1],   # rock
            11: [0.6, 0.8, 1.0],   # cave_ice
            12: [0.6, 0.1, 0.6],   # cave_mushroom
            13: [0.5, 0.5, 0.5],   # cave_normal
            14: [0.2, 0.8, 1.0],   # cave_crystal
            15: [1.0, 0.3, 0.0],   # cave_lava
            16: [0.0, 0.0, 0.0],   # air
        }

        img = np.zeros((SIZE, SIZE, 3))
        for biome_id, color in colors.items():
            mask = cave_biomes == biome_id
            img[mask] = color

        return img


    # ==============================================================================
    # MAIN (pour visualisation)
    # ==============================================================================

    def main():
        print("🌍 Génération du monde...")
        heightmap, humiditymap, temperaturemap, altitude_map = generate_overworld()
        biome_map = compute_biomes_vectorized(heightmap, humiditymap, temperaturemap)
        
        print("🏘️ Villages et grottes...")
        villages = generate_villages(biome_map)
        grottes = generate_grottes(biome_map)
        print(f"   → {len(villages)} villages")
        print(f"   → {len(grottes)} grottes")
        
        print("🕳️ Système souterrain...")
        cave_map, cave_noise, cave_biomes, biome_noise = generate_cave_system()
        
        print("🎨 Rendu...")
        img_over = render_overworld_map(biome_map, villages, grottes)
        img_cave = render_cave_map(cave_biomes)
        
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        axes[0].imshow(img_over)
        axes[0].set_title("Surface (villages=rouge, grottes=cyan)")
        axes[0].axis("off")
        
        axes[1].imshow(img_cave)
        axes[1].set_title("Souterrain")
        axes[1].axis("off")
        
        plt.tight_layout()
        plt.show()


    # ==============================================================================
    # GÉNÉRATION POUR LE JEU
    # ==============================================================================
        
    WORLD_FILE = "world_data.pkl"

    loaded = load_world(WORLD_FILE)

    if loaded:
        world_map, texture_variants, cave, coord_vil, coord_grottes, altitude_map = loaded
        print(f"🎮 Monde chargé : {SIZE}x{SIZE}")

    else:
        print("🌍 Génération du monde (première fois, ~5-10 secondes)...")

        # 1. Génération terrain de base
        heightmap, humiditymap, temperaturemap, altitude_map = generate_overworld()
        world_map = compute_biomes_vectorized(heightmap, humiditymap, temperaturemap)
        world_map, texture_variants = add_texture_variants(world_map)

        # 2. Falaises et passages
        print("🏔️ Détection des falaises...")
        cliff_edges = []
        print(f"   → {len(cliff_edges)} tiles de cliff détectées")

        print("🚪 Création des passages...")
        # 3. Grottes et villages
        cave = generate_cave_system()[2]
        coord_vil = generate_villages(world_map)
        coord_grottes = generate_grottes(world_map)

        # 4. Spawn point
        world_map[1510, 1510] = BIOME_IDS["collide"]

        # 5. Sauvegarder (AVEC les passages)
        save_world(WORLD_FILE, world_map, texture_variants, cave, coord_vil, coord_grottes, altitude_map)
        print(f"🎮 Monde généré : {SIZE}x{SIZE}")

        # Classification des villages (s'exécute toujours)
    print("\n Classification et génération des villages...")
    villages = classify_villages(coord_vil, world_map, nb_villes=3, rayon_proximite=1000)

    # Appliquer les bâtiments
    for village in villages:
        village.generate()
        for building in village.buildings:
            size = building.size
            for dy in range(size[1]):
                for dx in range(size[0]):
                    bx = building.x + dx
                    by = building.y + dy
                    if 0 <= bx < SIZE and 0 <= by < SIZE:
                        world_map[by, bx] = BIOME_IDS["collide"]

    print(f"   → {sum(1 for v in villages if v.type == 'city')} villes")

    # Gérer altitude_map si absent
    if altitude_map is None:
        print("⚠️ Ancienne sauvegarde sans altitude, régénération...")
        altitude_map = generate_overworld()[3]
        save_world(WORLD_FILE, world_map, texture_variants, cave, coord_vil, coord_grottes, altitude_map)

    # Export des variables (pour utilisation dans le jeu)
    if 'cliff_edges' not in locals():
        cliff_edges = []
    # 3. Créer les passages
    print("🚪 Création des passages...")
    
    
    # Filtrer cliff_edges pour enlever les passages
    cliff_edges = []
    print(f"   → {len(cliff_edges)} cliffs après passages")

    print(f"\n✅ Monde prêt :")
    print(f"   → {len(coord_vil)} villages")
    print(f"   → {len(coord_grottes)} grottes")
    print(f"   → {len(cliff_edges)} falaises")

    if __name__ == "__main__":
        main()

    return world_map, texture_variants, cave, coord_vil, coord_grottes, altitude_map, cliff_edges, villages


