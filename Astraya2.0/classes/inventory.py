import entity as ent
import texture
import settings

class Slot:
    def __init__(self):
        self.item = None
        self.quantity = 0

    def is_empty(self):
        return self.item is None

    def can_stack(self, item):
        return self.item == item and self.quantity < item.max_stack

    def clear(self):
        self.item = None
        self.quantity = 0

    def __repr__(self):
        if self.is_empty():
            return "Slot(vide)"
        return f"Slot({self.item.name} x{self.quantity})"


class Inventory:
    def __init__(self, size=20, hotbar_size=5):
        self.slots = [Slot() for _ in range(size)]
        self.hotbar_size = hotbar_size
        self.selected_hotbar = 0       # index du slot actif dans la hotbar
        
    # ex : print(player.inventory.hotbar)  # accès rapide à la hotbar ; le @property fak(fait que) player.inventory.hotbar() devient player.inventory.hotbar
    @property
    def hotbar(self):
        return self.slots[:self.hotbar_size]
    
    @property
    def selected_item(self):
        slot = self.slots[self.selected_hotbar]
        return slot.item if not slot.is_empty() else None

    def add_item(self, item, quantity=1):
        remaining = quantity

        # 1. Remplir les slots existants avec le même item
        for slot in self.slots:
            if remaining <= 0:
                break
            if slot.can_stack(item):
                space = item.max_stack - slot.quantity
                added = min(space, remaining)
                slot.quantity += added
                remaining -= added

        # 2. Remplir les slots vides
        for slot in self.slots:
            if remaining <= 0:
                break
            if slot.is_empty():
                slot.item = item
                added = min(item.max_stack, remaining)  # ← variable séparée
                slot.quantity = added
                remaining -= added                       # ← soustrait "added", pas "slot.quantity"

        return remaining

    def remove_item(self, item, quantity=1):
        """Retire un item. Retourne True si succès."""
        total = sum(s.quantity for s in self.slots if s.item == item)
        if total < quantity:
            return False

        remaining = quantity
        for slot in self.slots:
            if slot.item == item and remaining > 0:
                taken = min(slot.quantity, remaining)
                slot.quantity -= taken
                remaining -= taken
                if slot.quantity == 0:
                    slot.clear()
        return True

    def remove_slot_item(self, index, quantity=1):
        """Retire depuis un slot précis."""
        slot = self.slots[index]
        if slot.is_empty() or slot.quantity < quantity:
            return False
        slot.quantity -= quantity
        if slot.quantity == 0:
            slot.clear()
        return True

    def has_item(self, item, quantity=1):
        total = sum(s.quantity for s in self.slots if s.item == item)
        return total >= quantity

    def use_selected(self, user):
        """Utilise l'item du slot actif de la hotbar."""
        item = self.selected_item
        if item:
            result = item.on_use(user)
            if item.item_type.value == "consumable" and result:
                self.remove_at(self.selected_hotbar)
            return result
        return None

    def select_hotbar(self, index):
        if 0 <= index < self.hotbar_size:
            self.selected_hotbar = index

    def scroll_hotbar(self, direction):
        """direction = +1 ou -1"""
        self.selected_hotbar = (self.selected_hotbar + direction) % self.hotbar_size
    
    def drop_slot(self, slot_index, quantity=1):
        """Remove item from slot and return (item, quantity) for spawning in world. Returns None if slot empty or not enough."""
        if slot_index < 0 or slot_index >= len(self.slots):
            return None
        slot = self.slots[slot_index]
        if slot.is_empty() or slot.quantity < quantity:
            return None
        item = slot.item
        slot.quantity -= quantity
        if slot.quantity == 0:
            slot.clear()
        return (item, quantity)

    def drop_selected(self, quantity=1):
        """Drop from current hotbar slot. Returns (item, quantity) or None."""
        return self.drop_slot(self.selected_hotbar, quantity)

    def try_place_selected(self, current_map, tile_x, tile_y, block_grp, player_pos):
        """If selected item is a block, place it at (tile_x, tile_y). Returns True if placed."""
        from .items import ItemType
        item = self.selected_item
        player_x, player_y = player_pos
        player_tile_x, player_tile_y= player_x//32, player_y//32
        if abs(player_tile_x - tile_x) > settings.PLAYER_PLACE_RANGE or abs(player_tile_y - tile_y) > settings.PLAYER_PLACE_RANGE:
            return False
        
        if player_tile_x == tile_x and player_tile_y == tile_y:
            return False
        
        if item is None or getattr(item, "item_type", None) != ItemType.BLOCK:
            return False
        map_h, map_w = current_map.shape
        if tile_x < 0 or tile_y < 0 or tile_x >= map_w or tile_y >= map_h:
            print("Placement hors carte")
            return False
        # Don't place on ocean (0) or other blocking tiles if we want walkable placement only
        
        for block in block_grp:
            if block.tile_x == tile_x and block.tile_y == tile_y:
                return False
        block_grp.add(ent.Block(texture.BLOCK_TEXTURE[item.place_biome_id], current_map, x=tile_x, y =tile_y))
        self.remove_slot_item(self.selected_hotbar, 1)
        return True

    def __repr__(self): # print(repr(player.inventory)) → affiche le contenu de l'inventaire ; (tu te doute qu'on ne peut pas afficher des classes sans les représenter d'une manière lisible, du coup on fait ça)
        lines = [f"=== Inventaire ==="]
        for i, slot in enumerate(self.slots):
            prefix = ">" if i == self.selected_hotbar else " "
            hotbar_tag = "[hotbar]" if i < self.hotbar_size else ""
            lines.append(f"{prefix} [{i}] {slot} {hotbar_tag}")
        return "\n".join(lines)