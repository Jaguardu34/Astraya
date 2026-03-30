from enum import Enum
from classes.entity import Entity
import pygame


class ItemType(Enum):
    MISC = "misc"
    WEAPON = "weapon"
    TOOL = "tool"
    CONSUMABLE = "consumable"
    BLOCK = "block"


# classe mère de tous les items, les autres classes héritent de celle ci, elle contient les propriétés communes à tous les items (nom, type, etc.) et une méthode on_use() qui sera surchargée dans les sous-classes pour définir le comportement spécifique de chaque type d'item lorsqu'il est utilisé.
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
    def __init__(self, name, damage=1, attack_speed=1.0, range=32, texture_index=0):
        super().__init__(
            name, ItemType.WEAPON, max_stack=1, texture_index=texture_index
        )
        self.damage = damage
        self.attack_speed = attack_speed  # attaques par seconde
        self.range = range
        self.last_attack = 0

    def on_use(self, user) -> int:

        now = pygame.time.get_ticks()
        cooldown = int(1000 / self.attack_speed)
        if now - self.last_attack >= cooldown:
            self.last_attack = now
            return self.damage  # retourne les dégâts infligés
        return 0

    def __repr__(self):
        return f"Weapon({self.name}, dmg={self.damage})"


class Tool(Item):
    """o"""

    def __init__(
        self, name, efficiency=1.0, attack_speed=1.0, range=32, texture_index=0, tool_type=None
    ):
        super().__init__(name, ItemType.TOOL, max_stack=1, texture_index=texture_index)
        self.efficiency = efficiency
        self.cooldown = int(1000 / attack_speed)
        self.range = range
        self.last_use = 0
        self.tool_type = tool_type

    def on_use(self, user:Entity) -> bool:
        now = pygame.time.get_ticks()
        if now - self.last_use >= self.cooldown:
            self.last_use = now
            return True
        return False  # logique d'outil (miner, couper, etc.)

    def __repr__(self):
        return f"Tool({self.name}, eff={self.efficiency})"


class Consumable(Item):
    def __init__(self, name, heal=0, texture_index=0):
        super().__init__(
            name, ItemType.CONSUMABLE, max_stack=16, texture_index=texture_index
        )
        self.heal = heal

    def on_use(self, user):
        if hasattr(user, "hp"):
            user.hp = min(user.hp + self.heal, user.max_hp)
            return True  # consommé avec succès
        return False

    def __repr__(self):
        return f"Consumable({self.name}, heal={self.heal})"


class Block(Item):
    """Placeable block: on_place modifies the world map at (tile_x, tile_y)."""

    def __init__(self, name, place_biome_id, max_stack=64, texture_index=0):
        super().__init__(
            name, ItemType.BLOCK, max_stack=64, texture_index=texture_index
        )
        self.place_biome_id = (
            place_biome_id  # biome id to set when placed (e.g. plains=2, collide=7)
        )

    def on_use(self, user):
        """Place is handled by try_place_selected; use does nothing."""
        return None

    def __repr__(self):
        return f"Block({self.name}, biome_id={self.place_biome_id})"


# --- Registre des items existants dans le jeu ---
# pour créer un nouvel item, il suffit de l'ajouter dans ce dictionnaire avec une clé unique et une instance de la classe correspondante (Weapon, Tool ou Consumable).
ITEMS = {
    "wood_sword": Weapon("Épée en bois", damage=5, attack_speed=1.5, range=32),
    "stone_sword": Weapon("Épée en pierre", damage=10, attack_speed=1.2, range=32),
    "pickaxe": Tool("Pioche", efficiency=1.0),
    "axe": Tool("Hache", efficiency=1.0, tool_type="axe"),
    "bread": Consumable("Pain", heal=10),
    "apple": Consumable("Pomme", heal=5),
    "inoxible_axe": Tool("hache", efficiency=1.0, attack_speed=1.5, range=32),

    "wood": Item("Bois", ItemType.MISC, max_stack=64),
}


def get_item(name):
    item = ITEMS.get(name)
    if item is None:
        raise KeyError(f"Item inconnu : {name}")
    return item
