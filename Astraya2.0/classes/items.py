from enum import Enum

class ItemType(Enum):
    MISC = "misc"
    WEAPON = "weapon"
    TOOL = "tool"
    CONSUMABLE = "consumable"
    BLOCK = "block"
#classe mère de tous les items, les autres classes héritent de celle ci, elle contient les propriétés communes à tous les items (nom, type, etc.) et une méthode on_use() qui sera surchargée dans les sous-classes pour définir le comportement spécifique de chaque type d'item lorsqu'il est utilisé.
class Item:
    def __init__(self, name, item_type=ItemType.MISC, max_stack=64, texture_index=0):
        self.name = name
        self.item_type = item_type
        self.max_stack = max_stack
        self.texture_index = texture_index

    def on_use(self, user):
        """À surcharger dans les sous-classes."""
        pass

    def __repr__(self):
        return f"Item({self.name})"


class Weapon(Item):
    def __init__(self, name, damage = 1, attack_speed=1.0, range=32, texture_index=0):
        super().__init__(name, ItemType.WEAPON, max_stack=1, texture_index=texture_index)
        self.damage = damage
        self.attack_speed = attack_speed  # attaques par seconde
        self.range = range
        self.last_attack = 0

    def on_use(self, user):
        import pygame
        now = pygame.time.get_ticks()
        cooldown = int(1000 / self.attack_speed)
        if now - self.last_attack >= cooldown:
            self.last_attack = now
            return self.damage  # retourne les dégâts infligés
        return 0

    def __repr__(self):
        return f"Weapon({self.name}, dmg={self.damage})"


class Tool(Item):
    def __init__(self, name, efficiency=1.0, texture_index=0):
        super().__init__(name, ItemType.TOOL, max_stack=1, texture_index=texture_index)
        self.efficiency = efficiency

    def on_use(self, user):
        pass  # logique d'outil (miner, couper, etc.)

    def __repr__(self):
        return f"Tool({self.name}, eff={self.efficiency})"


class Consumable(Item):
    def __init__(self, name, heal=0, texture_index=0):
        super().__init__(name, ItemType.CONSUMABLE, max_stack=16, texture_index=texture_index)
        self.heal = heal

    def on_use(self, user):
        if hasattr(user, 'hp'):
            user.hp = min(user.hp + self.heal, user.max_hp)
            return True  # consommé avec succès
        return False

    def __repr__(self):
        return f"Consumable({self.name}, heal={self.heal})"
    
class Block(Item):
    """Placeable block: on_place modifies the world map at (tile_x, tile_y)."""
    def __init__(self, name, place_biome_id, max_stack=64, texture_index=0):
        super().__init__(name, ItemType.BLOCK, max_stack=64, texture_index=texture_index)
        self.place_biome_id = place_biome_id  # biome id to set when placed (e.g. plains=2, collide=7)

    def on_use(self, user):
        """Place is handled by try_place_selected; use does nothing."""
        return None

    def __repr__(self):
        return f"Block({self.name}, biome_id={self.place_biome_id})"


# --- Registre des items existants dans le jeu ---
# pour créer un nouvel item, il suffit de l'ajouter dans ce dictionnaire avec une clé unique et une instance de la classe correspondante (Weapon, Tool ou Consumable). 
ITEMS = {
    "wood_sword":   Weapon("Épée en bois",    damage=5,  attack_speed=1.5, range=32),
    "stone_sword":  Weapon("Épée en pierre",  damage=10, attack_speed=1.2, range=32),
    "pickaxe":      Tool("Pioche",            efficiency=1.0),
    "axe":          Tool("Hache",             efficiency=1.0),
    "bread":        Consumable("Pain",        heal=10),
    "apple":        Consumable("Pomme",       heal=5),
    # Placeable blocks (place_biome_id: 2=plains, 1=beach, 7=collide/solid)
    "grass_block":  Block("Bloc d'herbe",     place_biome_id=2, max_stack=64),
    "dirt_block":   Block("Bloc de terre",   place_biome_id=2, max_stack=64),
    "sand_block":   Block("Bloc de sable",   place_biome_id=1, max_stack=64),
    "stone_block":  Block("Truc rouge",  place_biome_id=7, max_stack=64),
    "forest_block": Block("bloc de forêt",  place_biome_id=4, max_stack=64),
    "water_block":  Block("eau",            place_biome_id=0, max_stack=64)
}

def get_item(name):
    item = ITEMS.get(name)
    if item is None:
        raise KeyError(f"Item inconnu : {name}")
    return item