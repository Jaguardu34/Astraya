import numpy as np
import math
import random
import matplotlib.pyplot as plt
import pickle
import os
from settings import *
import texture
from classes.village import *

def map_generate():
    
    global map, texture_variants, cave, coord_vil, coord_grottes, altitude_map, cliff_edges, villages
    
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

    def detect_cliff_edges(altitude_map, map):
        """Détecte les bords de falaises pour ajouter des textures de cliff."""
        
        cliffs_edges = {}  # {(x, y): ['N', 'S', 'E', 'W']}
        
        for y in range(SIZE): 
            for x in range(SIZE):
                current_alt = altitude_map[y, x]
                edges = []
                
                # Vérifier les 4 directions
                if y > 0 and altitude_map[y-1, x] < current_alt:  # ✅ y-1 pour Nord
                    edges.append('N')
                    map[y, x] = BIOME_IDS["cliff"]  # Marquer la tile comme cliff
                if y < SIZE-1 and altitude_map[y+1, x] < current_alt:  # ✅ y+1 pour Sud
                    edges.append('S')
                    map[y, x] = BIOME_IDS["cliff"]   
                if x > 0 and altitude_map[y, x-1] < current_alt:  # ✅ x-1 pour Ouest
                    edges.append('W')
                    map[y, x] = BIOME_IDS["cliff"] 
                if x < SIZE-1 and altitude_map[y, x+1] < current_alt:  # ✅ x+1 pour Est
                    edges.append('E')
                    map[y, x] = BIOME_IDS["cliff"] 
                
                if edges:
                    cliffs_edges[(x, y)] = edges
        
        print(f"Détecté {len(cliffs_edges)} tiles avec falaises")  # ✅ Print une seule fois
        return cliffs_edges

    def find_closed_zones(map, cliff_id):
        """
        Retourne une liste de zones fermées par des cliffs.
        Chaque zone est une liste de (x, y).
        """
        SIZE = map.shape[0]
        visited = [[False]*SIZE for _ in range(SIZE)]
        closed_zones = []

        def neighbors(x, y):
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < SIZE and 0 <= ny < SIZE:
                    yield nx, ny

        for y in range(SIZE):
            for x in range(SIZE):
                # On ignore les cliffs et les tiles déjà visitées
                if visited[y][x] or map[y][x] == cliff_id:
                    continue

                # Flood-fill avec une simple liste
                queue = [(x, y)]
                zone = []
                touches_border = False

                while queue:
                    cx, cy = queue[0]
                    queue = queue[1:]

                    if visited[cy][cx]:
                        continue
                    visited[cy][cx] = True
                    zone.append((cx, cy))

                    # Si la zone touche le bord → pas fermée
                    if cx == 0 or cy == 0 or cx == SIZE-1 or cy == SIZE-1:
                        touches_border = True

                    # Ajouter les voisins non-cliffs
                    for nx, ny in neighbors(cx, cy):
                        if not visited[ny][nx] and map[ny][nx] != cliff_id:
                            queue.append((nx, ny))

                # Si elle ne touche pas le bord → zone fermée
                if not touches_border:
                    closed_zones.append(zone)

        return closed_zones

    def compute_passage_count(zone_size):
        if zone_size < 200:
            return 20
        elif zone_size < 1000:
            return 100
        else:
            return 500


    def create_passages_for_zone(zone, map, cliff_id):
        """
        Crée des passages pour une zone fermée.
        
        ✅ CORRIGÉ : 
        - Trouve les bords de cliff adjacents à la zone
        - Crée des passages larges (3 tiles)
        - Vérifie que les passages sont bien créés
        """
        # 1. Trouver tous les bords de cliff adjacents à la zone
        cliff_borders = []
        
        for (x, y) in zone:
            # Vérifier les 4 voisins
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < SIZE and 0 <= ny < SIZE:
                    # Si le voisin est un cliff
                    if map[ny, nx] == cliff_id:
                        # Stocker : position dans zone, position cliff, direction
                        cliff_borders.append({
                            'zone_pos': (x, y),
                            'cliff_pos': (nx, ny),
                            'direction': (dx, dy)
                        })
        
        if not cliff_borders:
            print(f"   ⚠️ Aucun bord de cliff trouvé pour zone de {len(zone)} tiles")
            return 0
        
        # 2. Mélanger pour avoir des passages aléatoires
        random.shuffle(cliff_borders)
        
        # 3. Calculer le nombre de passages nécessaires
        zone_size = len(zone)
        passage_count = compute_passage_count(zone_size)
        
        # 4. Créer les passages
        created = 0
        attempted = 0
        max_attempts = min(len(cliff_borders), passage_count * 3)
        
        for border in cliff_borders:
            if created >= passage_count:
                break
            
            if attempted >= max_attempts:
                break
            
            attempted += 1
            
            if carve_passage(border, map, cliff_id):
                created += 1
        
        print(f"   ✅ {created}/{passage_count} passages créés pour zone de {zone_size} tiles")
        return created

    def carve_passage(border_info, map, cliff_id):
        """
        Crée un passage à travers un cliff.
        
        ✅ CORRIGÉ : 
        - Passage plus large (3 tiles de large)
        - Creuse suffisamment profond dans le cliff
        - Remplace par plains au lieu de garder le cliff
        
        Args:
            border_info: Dict avec 'zone_pos', 'cliff_pos', 'direction'
            map: La carte à modifier
            cliff_id: ID du biome cliff
        
        Returns:
            bool: True si le passage a été créé
        """
        zone_x, zone_y = border_info['zone_pos']
        cliff_x, cliff_y = border_info['cliff_pos']
        dx, dy = border_info['direction']
        
        passage_tiles = []
        
        # 1. Déterminer la direction perpendiculaire (pour élargir le passage)
        if dx != 0:  # Mouvement horizontal → élargir verticalement
            perp_dx, perp_dy = 0, 1
        else:  # Mouvement vertical → élargir horizontalement
            perp_dx, perp_dy = 1, 0
        
        # 2. Creuser un passage de 3 tiles de large et 5 tiles de profondeur
        width = 1  # ±1 tile de chaque côté = 3 tiles au total
        depth = 5  # Profondeur dans le cliff
        
        for d in range(depth):
            for w in range(-width, width + 1):
                px = cliff_x + dx * d + perp_dx * w
                py = cliff_y + dy * d + perp_dy * w
                
                # Vérifier limites
                if not (0 <= px < SIZE and 0 <= py < SIZE):
                    continue
                
                passage_tiles.append((px, py))
        
        # 3. Vérifier qu'on peut créer le passage
        if len(passage_tiles) < 3:
            return False
        
        # 4. Creuser le passage (remplacer par plains)
        for px, py in passage_tiles:
            map[py, px] = BIOME_IDS["plains"]
        
        return True

    #def carve_passage(x, y, cx, cy, map, cliff_id):
        SIZE = map.shape[0]

        dx = cx - x
        dy = cy - y

        # Normalisation stricte
        if abs(dx) > abs(dy):
            dx = 1 if dx > 0 else -1
            dy = 0
        else:
            dy = 1 if dy > 0 else -1
            dx = 0

        passage_tiles = []

        # 1) Casser la falaise côté zone
        entry_x = cx - dx
        entry_y = cy - dy
        if 0 <= entry_x < SIZE and 0 <= entry_y < SIZE:
            passage_tiles.append((entry_x, entry_y))

        # 2) Casser la falaise elle-même + 2 cases derrière
        for i in range(3):
            px = cx + dx * i
            py = cy + dy * i

            if not (0 <= px < SIZE and 0 <= py < SIZE):
                return False

            passage_tiles.append((px, py))

        # 3) Creuser
        for px, py in passage_tiles:
            map[py][px] = BIOME_IDS["plains"]

        return True


    def create_passages_simple(map, cliff_id, num_passages=100):
        """
        Crée des passages aléatoires dans les cliffs.
        
        ✅ AVANTAGES :
        - Très rapide (pas de flood-fill)
        - Garantit des passages
        - Simple à débugger
        
        Args:
            map: La carte de biomes
            cliff_id: ID du biome cliff
            num_passages: Nombre de passages à créer
        
        Returns:
            int: Nombre de tiles converties
        """
        # Trouver toutes les positions de cliff
        cliff_positions = np.argwhere(map == cliff_id)
        
        if len(cliff_positions) == 0:
            print("   ⚠️ Aucun cliff trouvé")
            return 0
        
        print(f"   📍 {len(cliff_positions)} tiles de cliff détectées")
        
        # Mélanger pour avoir des positions aléatoires
        np.random.shuffle(cliff_positions)
        
        tiles_converted = 0
        passages_created = 0
        
        # Créer des passages espacés
        spacing = max(1, len(cliff_positions) // num_passages)
        
        for i in range(0, len(cliff_positions), spacing):
            if passages_created >= num_passages:
                break
            
            y, x = cliff_positions[i]
            
            # Créer un passage de 3x3 tiles
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    px, py = x + dx, y + dy
                    
                    if 0 <= px < SIZE and 0 <= py < SIZE:
                        if map[py, px] == cliff_id:
                            map[py, px] = BIOME_IDS["plains"]
                            tiles_converted += 1
            
            passages_created += 1
        
        print(f"   ✅ {passages_created} passages créés ({tiles_converted} tiles converties)")
        return tiles_converted


    def compute_biomes_vectorized(heightmap, humiditymap, temperaturemap):
        """Calcule les biomes avec NumPy"""
        biomes = np.zeros((SIZE, SIZE), dtype=np.uint8)
        
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
        # Créer un array de variations (0-15 pour chaque tile)
        texture_variants = np.random.randint(0, 16, size=(SIZE, SIZE), dtype=np.uint8)
        
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
        map, texture_variants, cave, coord_vil, coord_grottes, altitude_map = loaded
        print(f"🎮 Monde chargé : {SIZE}x{SIZE}")
        
    else:
        print("🌍 Génération du monde (première fois, ~5-10 secondes)...")
        
        # 1. Génération terrain de base
        heightmap, humiditymap, temperaturemap, altitude_map = generate_overworld()
        map = compute_biomes_vectorized(heightmap, humiditymap, temperaturemap)
        map, texture_variants = add_texture_variants(map)
        
        # 2. Falaises et passages
        print("🏔️ Détection des falaises...")
        cliff_edges = detect_cliff_edges(altitude_map, map)
        print(f"   → {len(cliff_edges)} tiles de cliff détectées")
        
        print("🚪 Création des passages...")
        passages_count = create_passages_simple(map, BIOME_IDS["cliff"], num_passages=200)
        print(f"   → {passages_count} tiles converties en passages")
        
        # 3. Grottes et villages
        cave = generate_cave_system()[2]
        coord_vil = generate_villages(map)
        coord_grottes = generate_grottes(map)
        
        # 4. Spawn point
        map[1510, 1510] = BIOME_IDS["collide"]
        
        # 5. Sauvegarder (AVEC les passages)
        save_world(WORLD_FILE, map, texture_variants, cave, coord_vil, coord_grottes, altitude_map)
        print(f"🎮 Monde généré : {SIZE}x{SIZE}")

    # Classification des villages (s'exécute toujours)
    print("\n Classification et génération des villages...")
    villages = classify_villages(coord_vil, map, nb_cities, rayon_proximite=1000)

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
                        map[by, bx] = BIOME_IDS["collide"]

    print(f"   → {sum(1 for v in villages if v.type == 'city')} villes")

    # Gérer altitude_map si absent
    if altitude_map is None:
        print("⚠️ Ancienne sauvegarde sans altitude, régénération...")
        altitude_map = generate_overworld()[3]
        save_world(WORLD_FILE, map, texture_variants, cave, coord_vil, coord_grottes, altitude_map)

    # Export des variables (pour utilisation dans le jeu)
    if 'cliff_edges' not in locals():
        cliff_edges = detect_cliff_edges(altitude_map, map)

    # 3. Créer les passages
    print("🚪 Création des passages...")
    passages_count = create_passages_simple(map, BIOME_IDS["cliff"], num_passages=200)

    # ✅ AJOUTER CES LIGNES :
    # Filtrer cliff_edges pour enlever les passages
    cliff_edges = {
        (x, y): dirs 
        for (x, y), dirs in cliff_edges.items() 
        if map[y, x] == BIOME_IDS["cliff"]  # Toujours un cliff ?
    }
    print(f"   → {len(cliff_edges)} cliffs après passages")

    print(f"\n✅ Monde prêt :")
    print(f"   → {len(coord_vil)} villages")
    print(f"   → {len(coord_grottes)} grottes")
    print(f"   → {len(cliff_edges)} falaises")

    if __name__ == "__main__":
        main()
        
    return map, texture_variants, cave, coord_vil, coord_grottes, altitude_map, cliff_edges, villages


map = texture_variants = cave = coord_vil = coord_grottes = altitude_map = cliff_edges = villages = None