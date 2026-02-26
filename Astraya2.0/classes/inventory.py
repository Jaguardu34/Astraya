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
        """Ajoute un item. Retourne la quantité qui n'a pas pu être ajoutée."""
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
                slot.quantity = min(item.max_stack, remaining)
                remaining -= slot.quantity

        return remaining  # 0 si tout a été ajouté

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

    def __repr__(self): # print(repr(player.inventory)) → affiche le contenu de l'inventaire ; (tu te doute qu'on ne peut pas afficher des classes sans les représenter d'une manière lisible, du coup on fait ça)
        lines = [f"=== Inventaire ==="]
        for i, slot in enumerate(self.slots):
            prefix = ">" if i == self.selected_hotbar else " "
            hotbar_tag = "[hotbar]" if i < self.hotbar_size else ""
            lines.append(f"{prefix} [{i}] {slot} {hotbar_tag}")
        return "\n".join(lines)