"""
Inventory UI: hotbar (always visible) and full inventory panel (toggle with E).
Supports click-to-select, drop (Q), place block (right-click / R).
"""
import pygame
import os
from settings import ITEM_BOX_SIZE, HOTBAR_ACTIVE, BASE_DIR
from classes.items import ItemType

# Slot layout
SLOT_SIZE = 48
SLOT_MARGIN = 4
HOTBAR_SLOTS = 5
INVENTORY_COLS = 5
INVENTORY_ROWS = 4
PANEL_PADDING = 16

# Colors
SLOT_BG = (60, 60, 70)
SLOT_BORDER = (90, 90, 100)
SLOT_SELECTED = (255, 215, 0)
SLOT_HOVER = (120, 120, 130)
TEXT_COLOR = (240, 240, 240)
PANEL_BG = (40, 40, 50, 230)

# Item type colors for placeholder icons
ITEM_COLORS = {
    ItemType.WEAPON: (120, 100, 80),
    ItemType.TOOL: (100, 80, 60),
    ItemType.CONSUMABLE: (80, 140, 80),
    ItemType.BLOCK: (100, 70, 40),
    ItemType.MISC: (100, 100, 100),
}


def _get_font(size=16):
    for name in ("assets/fonts/joystix.ttf", "joystix.ttf", "../graphics/font/joystix.ttf"):
        font_path = os.path.join(BASE_DIR, name) if not name.startswith(".") else name
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
    return pygame.font.SysFont("arial", size)


def _item_icon_surface(item, size=40):
    """Simple colored icon for an item."""
    surf = pygame.Surface((size, size))
    color = ITEM_COLORS.get(getattr(item, "item_type", ItemType.MISC), (80, 80, 80))
    surf.fill(color)
    pygame.draw.rect(surf, (60, 60, 60), (0, 0, size, size), 2)
    font = _get_font(size // 2)
    letter = item.name[0].upper() if item.name else "?"
    text = font.render(letter, True, (255, 255, 255))
    tr = text.get_rect(center=(size // 2, size // 2))
    surf.blit(text, tr)
    return surf


def draw_slot(screen, rect, slot, selected, hovered, font):
    """Draw one inventory slot (background, border, optional item icon + count)."""
    color = SLOT_SELECTED if selected else (SLOT_HOVER if hovered else SLOT_BG)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, SLOT_BORDER, rect, 2)
    if slot and not slot.is_empty():
        icon = _item_icon_surface(slot.item, rect.width - 8)
        screen.blit(icon, (rect.x + 4, rect.y + 4))
        if slot.quantity > 1:
            count_text = font.render(str(slot.quantity), True, TEXT_COLOR)
            screen.blit(count_text, (rect.right - count_text.get_width() - 4, rect.bottom - count_text.get_height() - 2))


def draw_hotbar(screen, inventory):
    """Draw the hotbar at the bottom center of the screen."""
    font = _get_font(14)
    w, h = screen.get_size()
    total_width = HOTBAR_SLOTS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
    start_x = (w - total_width) // 2
    start_y = h - SLOT_SIZE - 20
    for i in range(HOTBAR_SLOTS):
        rect = pygame.Rect(start_x + i * (SLOT_SIZE + SLOT_MARGIN), start_y, SLOT_SIZE, SLOT_SIZE)
        slot = inventory.slots[i]
        draw_slot(screen, rect, slot, selected=(i == inventory.selected_hotbar), hovered=False, font=font)


def draw_inventory_panel(screen, inventory, mouse_pos, selected_slot=None):
    """Draw full inventory panel (grid). selected_slot: slot index to highlight for drop (when panel open)."""
    font = _get_font(14)
    w, h = screen.get_size()
    panel_width = INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN + PANEL_PADDING * 2
    panel_height = INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN + PANEL_PADDING * 2 + 30
    panel_rect = pygame.Rect((w - panel_width) // 2, (h - panel_height) // 2, panel_width, panel_height)
    s = pygame.Surface((panel_width, panel_height))
    s.set_alpha(230)
    s.fill((40, 40, 50))
    screen.blit(s, panel_rect)
    pygame.draw.rect(screen, (80, 80, 90), panel_rect, 3)
    title_font = _get_font(20)
    title = title_font.render("Inventaire (E fermer, Q drop, R place)", True, TEXT_COLOR)
    screen.blit(title, (panel_rect.x + PANEL_PADDING, panel_rect.y + 4))
    grid_left = panel_rect.x + PANEL_PADDING
    grid_top = panel_rect.y + 30 + PANEL_PADDING
    for row in range(INVENTORY_ROWS):
        for col in range(INVENTORY_COLS):
            idx = row * INVENTORY_COLS + col
            if idx >= len(inventory.slots):
                break
            rect = pygame.Rect(
                grid_left + col * (SLOT_SIZE + SLOT_MARGIN),
                grid_top + row * (SLOT_SIZE + SLOT_MARGIN),
                SLOT_SIZE,
                SLOT_SIZE,
            )
            slot = inventory.slots[idx]
            hovered = rect.collidepoint(mouse_pos)
            is_selected = (selected_slot is not None and idx == selected_slot) or (
                selected_slot is None and idx == inventory.selected_hotbar and idx < inventory.hotbar_size
            )
            draw_slot(screen, rect, slot, selected=is_selected, hovered=hovered, font=font)


def get_hotbar_slot_at(mouse_pos, screen_size):
    """Return hotbar slot index (0..HOTBAR_SLOTS-1) if mouse is over hotbar, else None."""
    w, h = screen_size
    start_x = (w - (HOTBAR_SLOTS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN)) // 2
    start_y = h - SLOT_SIZE - 20
    for i in range(HOTBAR_SLOTS):
        rect = pygame.Rect(start_x + i * (SLOT_SIZE + SLOT_MARGIN), start_y, SLOT_SIZE, SLOT_SIZE)
        if rect.collidepoint(mouse_pos):
            return i
    return None


def get_panel_slot_at(mouse_pos, screen_size):
    """Return inventory slot index if mouse is over the open panel grid, else None."""
    w, h = screen_size
    panel_width = INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN + PANEL_PADDING * 2
    panel_height = INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN + PANEL_PADDING * 2 + 30
    grid_left = (w - panel_width) // 2 + PANEL_PADDING
    grid_top = (h - panel_height) // 2 + 30 + PANEL_PADDING
    for row in range(INVENTORY_ROWS):
        for col in range(INVENTORY_COLS):
            idx = row * INVENTORY_COLS + col
            rect = pygame.Rect(
                grid_left + col * (SLOT_SIZE + SLOT_MARGIN),
                grid_top + row * (SLOT_SIZE + SLOT_MARGIN),
                SLOT_SIZE,
                SLOT_SIZE,
            )
            if rect.collidepoint(mouse_pos):
                return idx
    return None
