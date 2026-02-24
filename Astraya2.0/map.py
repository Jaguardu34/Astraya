import numpy as np
import random

SIZE = 2000

collide_tiles = [3]

# --- 1. Bruit Perlin-like vectorisé ---
def perlin(width, height, scale=10, seed=0):
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


# --- 2. Bruit fractal pour continents ---
def fractal_noise(scale, seed):
    base = perlin(SIZE, SIZE, scale=scale, seed=seed)
    mid  = perlin(SIZE, SIZE, scale=scale//2, seed=seed+1) * 0.5
    fine = perlin(SIZE, SIZE, scale=scale//4, seed=seed+2) * 0.25
    return base + mid + fine


# --- 3. Génération des continents ---
heightmap = fractal_noise(scale=300, seed=1)
humiditymap = fractal_noise(scale=500, seed=2)
temperaturemap = fractal_noise(scale=500, seed=3)

# Normalisation
def norm(a):
    return (a - a.min()) / (a.max() - a.min())

heightmap = norm(heightmap)
humiditymap = norm(humiditymap)
temperaturemap = norm(temperaturemap)


# --- 4. Biomes ---
def compute_biomes(heightmap, humiditymap, temperaturemap):
    biomes = [["" for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(SIZE):
        for x in range(SIZE):
            h = heightmap[y][x]
            hum = humiditymap[y][x]
            temp = temperaturemap[y][x]

            if h < 0.35:
                biome = "ocean"
            elif h < 0.40:
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


# --- 5. Résultat final : liste de listes ---
biome_map = compute_biomes(heightmap, humiditymap, temperaturemap)
map = biome_map


nb_villages = 80
coord_vil = []

for vil in range(nb_villages):
    posable = False

    while not posable:
        cord_vil_x = random.randint(0, SIZE)
        cord_vil_y = random.randint(0,SIZE)
        if map[cord_vil_x][cord_vil_y] != 0:
            coord_vil.append([cord_vil_x, cord_vil_y])
            posable = True
            
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == "plains":
            x_text = random.randint(1,3)
            if x_text == 1:
                map[i][j] = "plains_1"
            elif x_text == 2:
                map[i][j] = "plains_2"
            else : 
                map[i][j] = "plains_3"



