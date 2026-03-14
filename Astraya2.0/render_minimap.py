import numpy as np
import pickle
from PIL import Image
import os

minimap_path = "Astraya2.0/minimap.png"
world_path = "world_data.pkl"

def generate_minimap():
    if (not os.path.exists(minimap_path) or 
        os.path.getmtime(world_path) > os.path.getmtime(minimap_path)):
        # régénère
        TILE_COLORS = {
            0:  (0, 76, 153),
            1:  (237, 201, 120),
            2:  (100, 180, 80),
            3:  (144, 238, 144),
            4:  (0, 100, 0),
            5:  (128, 128, 128),
            6:  (255, 255, 255),
            7:  (255, 0, 0),
            10: (50, 50, 50),
            11: (180, 220, 255),
            12: (150, 0, 150),
            13: (120, 120, 120),
            14: (0, 200, 255),
            15: (255, 80, 0),
        }

        with open("world_data.pkl", "rb") as f:
            world_data = pickle.load(f)

        world_array = np.array(world_data['biome_map'])
        h, w = world_array.shape
        img_array = np.zeros((h, w, 3), dtype=np.uint8)

        for tile_id, color in TILE_COLORS.items():
            mask = world_array == tile_id
            img_array[mask] = color

        img = Image.fromarray(img_array, "RGB")
        img.save("Astraya2.0/minimap.png")
        print(f"Minimap générée : {w}x{h} pixels")
        
    else:
        print("Minimap à jour.")