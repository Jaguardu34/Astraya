import numpy as np
import pickle
from PIL import Image
import os
import texture

minimap_path = "sources/assets/minimap.png"
world_path = "sources/assets/world_data.pkl"

def generate_minimap():
    if (not os.path.exists(minimap_path) or 
        os.path.getmtime(world_path) > os.path.getmtime(minimap_path)):
        # régénère

        with open(world_path, "rb") as f:
            world_data = pickle.load(f)

        world_array = np.array(world_data['biome_map'])
        h, w = world_array.shape
        img_array = np.zeros((h, w, 3), dtype=np.uint8)

        for tile_id, color in texture.TILE_COLORS.items():
            mask = world_array == tile_id
            img_array[mask] = color

        img = Image.fromarray(img_array, "RGB")
        img.save(minimap_path)
        print(f"Minimap générée : {w}x{h} pixels")
        
    else:
        print("Minimap à jour.")