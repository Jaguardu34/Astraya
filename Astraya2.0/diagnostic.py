import numpy as np
import pickle

print("="*70)
print("VÉRIFICATION DES PASSAGES")
print("="*70)

# Charger le monde
with open('world_data.pkl', 'rb') as f:
    data = pickle.load(f)

map_data = data['biome_map']

print("\nCOMPTAGE DES BIOMES :")
print(f"  Cliffs (ID 70)  : {np.sum(map_data == 70):6d} tiles")
print(f"  Plains (ID 2)   : {np.sum(map_data == 2):6d} tiles")

# Trouver des positions de cliffs
cliff_positions = np.argwhere(map_data == 70)
plains_positions = np.argwhere(map_data == 2)

if len(cliff_positions) > 0:
    print(f"\n📍 Exemples de positions de CLIFFS :")
    for i in range(min(5, len(cliff_positions))):
        y, x = cliff_positions[i]
        print(f"   ({x:4d}, {y:4d})")

if len(plains_positions) > 0:
    print(f"\n📍 Exemples de positions de PLAINS :")
    for i in range(min(5, len(plains_positions))):
        y, x = plains_positions[i]
        print(f"   ({x:4d}, {y:4d})")

# Vérifier si des plains sont à côté de cliffs (= passages probables)
print(f"\n🔍 RECHERCHE DE PASSAGES (plains à côté de cliffs)...")

passages_found = 0
for i in range(min(1000, len(plains_positions))):
    y, x = plains_positions[i]
    
    # Vérifier les 8 voisins
    has_cliff_neighbor = False
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            
            ny, nx = y + dy, x + dx
            if 0 <= ny < 2000 and 0 <= nx < 2000:
                if map_data[ny, nx] == 70:  # Cliff voisin
                    has_cliff_neighbor = True
                    break
        if has_cliff_neighbor:
            break
    
    if has_cliff_neighbor:
        passages_found += 1
        if passages_found <= 5:
            print(f"   Passage potentiel trouvé à ({x:4d}, {y:4d})")

print(f"\n✅ TOTAL : ~{passages_found} plains à côté de cliffs")

if passages_found > 100:
    print("\n✅ CONCLUSION : Les passages EXISTENT dans la map !")
    print("   → Le problème est dans le RENDU")
    print("   → Les textures de cliff sont probablement dessinées par-dessus")
else:
    print("\n❌ CONCLUSION : Peu ou pas de passages dans la map")
    print("   → create_passages_simple() ne s'exécute pas correctement")

print("\n" + "="*70)
