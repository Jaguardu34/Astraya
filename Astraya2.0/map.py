import numpy as np
import random
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURATION
# ==============================================================================
SIZE = 2000
NB_VILLAGES = 80

# ==============================================================================
# GÉNÉRATION DE BRUIT PERLIN
# ==============================================================================

def perlin(width, height, scale=10, seed=0):
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
    """
    Crée un masque radial pour forcer les bords à être de l'océan.
    
    Args:
        size: Taille de la carte
        falloff: Contrôle la douceur de la transition (0.1 = bords durs, 0.5 = doux)
    
    Returns:
        Masque normalisé entre 0 (bords) et 1 (centre)
    """
    # Créer une grille de coordonnées centrées
    y, x = np.ogrid[0:size, 0:size]
    center = size / 2
    
    # Distance normalisée au centre (0 au centre, 1 aux coins)
    dx = (x - center) / center
    dy = (y - center) / center
    distance = np.sqrt(dx**2 + dy**2)
    
    # Appliquer une fonction smooth pour la transition
    # Plus falloff est petit, plus la transition est abrupte
    mask = np.clip(1 - (distance - (1 - falloff)) / falloff, 0, 1)
    
    return mask


# ==============================================================================
# MONDE DE SURFACE
# ==============================================================================

def generate_overworld():
    """Génère les cartes de hauteur, humidité et température avec masque d'île."""
    heightmap = fractal_noise(scale=300, seed=1)
    humiditymap = fractal_noise(scale=500, seed=2)
    temperaturemap = fractal_noise(scale=500, seed=3)
    
    # Créer le masque d'île
    island_mask = create_island_mask(SIZE, falloff=0.4)
    
    # Appliquer le masque à la heightmap pour créer l'île
    heightmap = norm(heightmap)
    heightmap = heightmap * island_mask  # Multiplie par le masque (0 aux bords)
    
    return heightmap, norm(humiditymap), norm(temperaturemap)


def compute_biomes(heightmap, humiditymap, temperaturemap):
    """Calcule les biomes."""
    biomes = [["" for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(SIZE):
        for x in range(SIZE):
            h = heightmap[y][x]
            hum = humiditymap[y][x]
            temp = temperaturemap[y][x]

            if h < 0.25:
                biome = "ocean"
            elif h < 0.32:
                biome = "beach"
            elif h < 0.65:
                if hum > 0.6 and temp > 0.5:
                    biome = "jungle"
                elif hum > 0.4 and temp > 0.3:
                    biome = "forest"
                else:
                    biome = "plains"
            elif h < 0.80:
                biome = "mountains"
            else:
                biome = "snow_peak"

            biomes[y][x] = biome

    return biomes


# ==============================================================================
# GROTTES
# ==============================================================================

def generate_cave_system():
    """Génère le système de grottes."""
    cave_noise = (
        perlin(SIZE, SIZE, scale=80, seed=100) * 0.6 +
        perlin(SIZE, SIZE, scale=40, seed=101) * 0.3 +
        perlin(SIZE, SIZE, scale=20, seed=102) * 0.1
    )
    cave_noise = norm(cave_noise)

    cave_map = [
        ["air" if cave_noise[y][x] < 0.50 else "rock"
         for x in range(SIZE)]
        for y in range(SIZE)
    ]

    biome_noise = (
        perlin(SIZE, SIZE, scale=120, seed=300) * 0.6 +
        perlin(SIZE, SIZE, scale=60, seed=301) * 0.3 +
        perlin(SIZE, SIZE, scale=30, seed=302) * 0.1
    )
    biome_noise = norm(biome_noise)

    cave_biomes = [["" for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(SIZE):
        for x in range(SIZE):
            if cave_map[y][x] == "rock":
                cave_biomes[y][x] = "rock"
                continue

            n = biome_noise[y][x]
            if n < 0.20:
                cave_biomes[y][x] = "cave_ice"
            elif n < 0.40:
                cave_biomes[y][x] = "cave_mushroom"
            elif n < 0.60:
                cave_biomes[y][x] = "cave_normal"
            elif n < 0.80:
                cave_biomes[y][x] = "cave_crystal"
            else:
                cave_biomes[y][x] = "cave_lava"

    return cave_biomes


# ==============================================================================
# VILLAGES
# ==============================================================================

def generate_villages(biome_map, nb_villages=NB_VILLAGES):
    """Place des villages en évitant l'océan."""
    coord_vil = []

    for _ in range(nb_villages):
        attempts = 0
        trouve = False
        while attempts < 10000 and not trouve:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            
            if biome_map[y][x] != "ocean":
                coord_vil.append([x, y])
                trouve = True
            attempts += 1

    return coord_vil


# ==============================================================================
# Grottes
# ==============================================================================

def generate_grottes(biome_map, nb_grottes=NB_VILLAGES):
    """Place des villages en évitant l'océan."""
    coord_grottes = [[1500, 1501]]

    for _ in range(nb_grottes):
        attempts = 0
        trouve = False
        while attempts < 10000 and not trouve:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            
            if biome_map[y][x] != "ocean":
                coord_grottes.append([x, y])
                trouve = True
            attempts += 1

    return coord_grottes


# ==============================================================================
# RENDU
# ==============================================================================

def render_overworld_map(biome_map, village_coords=None, grottes_coords=None):
    """Génère l'image de surface."""
    colors = {
        "ocean": [0.0, 0.3, 1.0],
        "beach": [1.0, 0.9, 0.6],
        "jungle": [0.1, 0.5, 0.1],
        "forest": [0.05, 0.3, 0.05],
        "plains": [0.5, 0.8, 0.2],
        "mountains": [0.5, 0.5, 0.5],
        "snow_peak": [1.0, 1.0, 1.0],
    }

    img = np.zeros((SIZE, SIZE, 3))
    for y in range(SIZE):
        for x in range(SIZE):
            img[y][x] = colors[biome_map[y][x]]

    if village_coords:
        for x, y in village_coords:
            if 0 <= y < SIZE and 0 <= x < SIZE:
                img[y][x] = [1.0, 0.0, 0.0]

    if grottes_coords:
        for x, y in grottes_coords:
            if 0 <= y < SIZE and 0 <= x < SIZE:
                img[y][x] = [0,6, 1.0, 1.0]

    return img


def render_cave_map(cave_biomes):
    """Génère l'image souterraine."""
    colors = {
        "rock": [0.1, 0.1, 0.1],
        "cave_normal": [0.5, 0.5, 0.5],
        "cave_mushroom": [0.6, 0.1, 0.6],
        "cave_crystal": [0.2, 0.8, 1.0],
        "cave_lava": [1.0, 0.3, 0.0],
        "cave_ice": [0.6, 0.8, 1.0],
    }

    img = np.zeros((SIZE, SIZE, 3))
    for y in range(SIZE):
        for x in range(SIZE):
            img[y][x] = colors[cave_biomes[y][x]]

    return img


# ==============================================================================
# MAIN Juste pour generer que les map, hors code
# ==============================================================================

def main():
    print("Génération du monde...")
    heightmap, humiditymap, temperaturemap = generate_overworld()
    biome_map = compute_biomes(heightmap, humiditymap, temperaturemap)
    
    print("Villages...")
    villages = generate_villages(biome_map)
    grottes = generate_grottes(biome_map)
    print(f"→ {len(villages)} villages")
    
    print("Grottes...")
    cave_map, cave_noise, cave_biomes, biome_noise = generate_cave_system()
    
    print("Rendu...")
    img_over = render_overworld_map(biome_map, villages, grottes)
    img_cave = render_cave_map(cave_biomes)
    
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    axes[0].imshow(img_over)
    axes[0].set_title("Surface (villages en rouge)")
    axes[0].axis("off")
    
    axes[1].imshow(img_cave)
    axes[1].set_title("Souterrain")
    axes[1].axis("off")
    
    plt.tight_layout()
    plt.show()
    
    return biome_map, villages, cave_biomes

if __name__ == "__main__":
    main()
    
    
#map de test (j'en ai besoin)


print("Génération du monde...")
heightmap, humiditymap, temperaturemap = generate_overworld()
map = compute_biomes(heightmap, humiditymap, temperaturemap)
cave = generate_cave_system()
coord_vil = generate_villages(map)
coord_grottes = generate_grottes(map)

# Tiles sur lesquelles on ne peut pas marcher
collide_tiles = ["ocean", "collide"]

print(f"Monde généré : {SIZE}x{SIZE}")
print(f"{len(coord_vil)} villages placés")
print(coord_grottes)


for i in range(len(map)):
    for j in range(len(map[i])):
        if map[j][i] == "plains":
            x = random.randint(0, 15)
            map[j][i] = f"plains*{x}"
            
for i in range(len(map)):
    for j in range(len(map[i])):
        if map[j][i] == "beach":
            x = random.randint(0, 15)
            map[j][i] = f"beach*{x}"


map[1510][1510] = "collide"