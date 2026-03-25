import math
import os
import random
import threading
<<<<<<< HEAD

=======
import render_minimap
from ui import interfaces
import world_data
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
import generate_map
import interfaces
import map_render
import numpy as np
import pygame
import render_minimap
import settings
import texture
import world_data
from classes import animals, ennemy, entity, items, npc, objects
from classes import player as player_class
from classes import quest as quest_module
from classes import village as village
<<<<<<< HEAD
=======
from classes import boss
import math
from ui import debug
from ui import ui_inventory
from ui import coeurs
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
from classes.items import get_item
from corruption import generer_corruption
from ui import debug, ui_inventory


class Chunk:
    def __init__(self, chunk_size=32):
        self.chunk_size = chunk_size
        self.grid = {}
        self._entity_chunk = {}  # entity → (cx, cy) dernier connu

    def get_chunk(self, x, y):
        return (int(x // self.chunk_size), int(y // self.chunk_size))

    def clear(self):
        self.grid.clear()
        self._entity_chunk.clear()

    def insert(self, entity):
        chunk = self.get_chunk(entity.x, entity.y)
        if chunk not in self.grid:
            self.grid[chunk] = []
        self.grid[chunk].append(entity)
        self._entity_chunk[id(entity)] = chunk

    def update_entity(self, entity):
        new_chunk = self.get_chunk(entity.x, entity.y)
        old_chunk = self._entity_chunk.get(id(entity))

        if old_chunk == new_chunk:
            return  # pas bougé de chunk, rien à faire

        if old_chunk is not None and old_chunk in self.grid:
            try:
                self.grid[old_chunk].remove(entity)
            except ValueError:
                pass
            if not self.grid[old_chunk]:
                del self.grid[old_chunk]

        if new_chunk not in self.grid:
            self.grid[new_chunk] = []
        self.grid[new_chunk].append(entity)
        self._entity_chunk[id(entity)] = new_chunk

    def remove_entity(self, entity):
        old_chunk = self._entity_chunk.pop(id(entity), None)
        if old_chunk and old_chunk in self.grid:
            try:
                self.grid[old_chunk].remove(entity)
            except ValueError:
                pass
            if not self.grid[old_chunk]:
                del self.grid[old_chunk]

    def get_nearby(self, x, y):
        cx, cy = self.get_chunk(x, y)
        nearby = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                chunk = (cx + dx, cy + dy)
                if chunk in self.grid:
                    nearby.extend(self.grid[chunk])
        return nearby


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.joystick.init()

        # sound
        sound_dir = "Astraya2.0/assets/sound"
        self.playlist = [
            os.path.join(sound_dir, f)
            for f in os.listdir(sound_dir)
            if f.endswith(".wav") or f.endswith(".mp3") or f.endswith(".ogg")
        ]

        self.current_music_index = 0
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        # lance la première
        pygame.mixer.music.load(
            self.playlist[random.randint(0, len(self.playlist) - 1)]
        )
        pygame.mixer.music.play()

        self.world_ready = False

        # pr charger la map en arriere plan
        thread = threading.Thread(target=self._load_world)
        thread.daemon = True
        thread.start()

        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGTH),
            pygame.RESIZABLE,
            pygame.OPENGL,
        )
        self.WINDOW_SCALE = self.screen.get_width(), self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.scale_main_map = (
            int(self.WINDOW_SCALE[0] // 32),
            int((self.WINDOW_SCALE[1] - 200) // 32),
        )
        self.render_distance = self.WINDOW_SCALE[0] // 2

        self.game_map = None
        self.current_map = None

        self.last_map_change = pygame.time.get_ticks()
        self.font_to_write = pygame.font.SysFont(None, 24)
        self.chunk_grid = Chunk(chunk_size=64)
        self.in_menu = False
        self.in_dungeon = False
        self.dungeon_map = None

<<<<<<< HEAD
        self.quest_manager = quest_module.QuestManager()

        # interface
=======

        #interface
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
        self.menu = interfaces.MainMenu()
        self.loadingscreen = interfaces.LoadingScreen()
        self.settings_menu = interfaces.SettingsMenu()

        # inventaire
        self.inventory_open = False
        self.panel_selected_slot = None

        self.sprites_initialized = False
        self.running = True

        self.music_playing = False

        self.joystick = False

        self.quest_init = False

        self.info_swipe = [True, 0, 300, pygame.time.get_ticks()]
        
        self.coeurs = coeurs.Coeurs()

    # charger la map gigantesque de Pau en arriere plan
    def _load_world(self):

        (
            world_data.world_map,
            world_data.texture_variants,
            world_data.cave,
            world_data.coord_vil,
            world_data.coord_grottes,
            world_data.altitude_map,
            world_data.cliff_edges,
            world_data.villages,
            world_data.origin_donjon_coords,
            world_data.donjons_maps,
        ) = generate_map.map_generate()

        if not world_data.donjons_maps:
            print("⚠️ Ancienne sauvegarde sans donjons, régénération...")
            _, _, world_data.donjons_maps = generer_corruption(
                world_data.world_map, nb_zones=5
            )

        render_minimap.generate_minimap()
        self.dungeon_map = world_data.donjons_maps[0]

        if world_data.world_map is not None:
            self.world_ready = True
        else:
            self.world_ready = False

    # creer tt les entity et les mettre dans un sprite.group
    def init_sprites(self):
        print("Initialisation des sprites...")

        self.projectile_grp = pygame.sprite.Group()
        self.entity_grp = pygame.sprite.Group()
        self.ennemy_grp = pygame.sprite.Group()
        self.dropped_grp = pygame.sprite.Group()
        self.block_grp = pygame.sprite.Group()
        self.plant_grp = pygame.sprite.Group()
        self.npc_grp = pygame.sprite.Group()

        game_map = world_data.world_map
        alt = world_data.altitude_map

        self.alt = alt

        if game_map is None or alt is None:
            return

        self.game_map = game_map
        self.current_map = self.game_map

        # Charger les maps de donjons
        self.dungeon_maps = world_data.donjons_maps

<<<<<<< HEAD
        self.player = player_class.Player(
            texture.texture_player, self.game_map, alt, x=1500, y=1500
        )
=======
        self.player = player_class.Player(texture.texture_player, self.game_map, alt, x=1500, y=1500)
        self.quest_manager = quest_module.QuestManager(self.player)

        
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
        self.entity_grp.add(self.player)
        self.entity_grp.add(
            objects.Grotte(texture.texture_grotte, self.game_map, alt, x=1520, y=1450)
        )
        self.old_npc = npc.Npc(
            "spawn NPC",
            texture.texture_old_npc,
            self.game_map,
            ["Salut je suis un npc", "C'est tout ce que j'ai a dire"],
            x=1512,
            y=1512,
        )
        self.npc_grp.add(self.old_npc)
        for villager in village.spawn_villageois(world_data.villages[0], self.game_map):
            self.npc_grp.add(villager)

        # Surface pour la porte d'entrée
        door_surface = pygame.Surface((32, 32))
        door_surface.fill((150, 75, 0))  # marron

        self.entity_grp.add(
            entity.DungeonDoor([door_surface], self.game_map, alt, x=1502, y=1500)
        )

        # for donjons in world_data.origin_donjon_coords:
        #    self.entity_grp.add(entity.DungeonDoor([door_surface], self.game_map, alt, x=donjons[0], y=donjons[1]))

<<<<<<< HEAD
        # Items de départ
        self.player.inventory.add_item(get_item("wood_sword"), 1)
        self.player.inventory.add_item(get_item("bread"), 3)
        self.player.inventory.add_item(get_item("inoxible_axe", 1))
=======
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b

        # Plantes
        valid_mask_plant = np.isin(self.game_map, [2, 3, 4])
        valid_positions_plant = np.argwhere(valid_mask_plant)

<<<<<<< HEAD
        rng = np.random.default_rng()
        indices = rng.choice(
            len(valid_positions), size=min(5000, len(valid_positions)), replace=False
        )

        for idx in indices:
            y_plant, x_plant = valid_positions[idx]
            self.plant_grp.add(
                objects.Plant(
                    texture.texture_plant,
                    self.game_map,
                    8,
                    alt,
                    x=int(x_plant),
                    y=int(y_plant),
                )
            )
=======
        rng_plant = np.random.default_rng()
        indices_plant = rng_plant.choice(len(valid_positions_plant), size=min(5000, len(valid_positions_plant)), replace=False)
        
        

        for idx in indices_plant:
            y_plant, x_plant = valid_positions_plant[idx]
            self.plant_grp.add(objects.Plant(texture.texture_plant, self.game_map, 8, alt, x=int(x_plant), y=int(y_plant)))
            
        # Arbres
        valid_mask_tree = np.isin(self.game_map, [2, 3, 4])
        valid_positions_tree = np.argwhere(valid_mask_tree)

        rng_tree = np.random.default_rng()
        indices_tree = rng_tree.choice(len(valid_positions_tree), size=min(5000, len(valid_positions_tree)), replace=False)
        
        for idx in indices_tree:
            y_tree, x_tree = valid_positions_tree[idx]
            self.plant_grp.add(objects.Tree(texture.texture_tree, self.game_map, alt, x=int(x_tree), y=int(y_tree)))
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b

        # Ennemis et animaux
        for i in range(20):
            self.ennemy_grp.add(
                ennemy.Corrupted_Chicken(
                    texture.texture_chicken_corrupted,
                    self.current_map,
                    self.player,
                    self.projectile_grp,
                    alt,
                    1410,
                    1400,
                )
            )

        for i in range(100):
            x = random.randint(1300, 1600)
            y = random.randint(1300, 1600)
            if entity.veriftile(x, y, self.game_map) is True:
                self.entity_grp.add(
                    animals.Chicken(
                        texture.texture_chicken, self.game_map, alt, x=x, y=y
                    )
                )

        for i in range(100):
            x = random.randint(1300, 1600)
            y = random.randint(1300, 1600)
            if entity.veriftile(x, y, self.game_map) is True:
                self.entity_grp.add(
                    animals.Cow(texture.texture_cow, self.game_map, alt, x=x, y=y)
                )

        self.plant_index_built = False
        self._chunk_registered = False  # changer de map

    def change_map(self):
        change_cooldown = 2000
        now = pygame.time.get_ticks()
        if now - self.last_map_change >= change_cooldown:
            if self.current_map is self.game_map:
                self.current_map = world_data.cave
            else:
                self.current_map = self.game_map
            self.last_map_change = now

    # afficher les fps et coord
    def draw_infos(self, x, y, pos):
        fps = self.clock.get_fps()
        text = self.font_to_write.render(
            f"Coordinates: (x: {int(pos[0]) // 32}, y: {int(pos[1]) // 32})",
            True,
            "black",
        )
        text_fps = self.font_to_write.render(f"FPS : {fps:.2f}", True, "black")
        pygame.display.set_caption(f"Astraya 2.0 - FPS : {fps:.2f}", "Astraya")
        self.screen.blit(text, (x, y))
        self.screen.blit(text_fps, (x, y + self.font_to_write.size("A")[1] + 2))

    # update les chunk aux alentours
    def register_all_entities(self, sprite_group_to_add):

        self.chunk_grid.clear()
        self.chunk_grid.insert(self.player)
        for group in sprite_group_to_add:
            for sprite in group:
                self.chunk_grid.insert(sprite)

    def update_chunk(self, sprite_group_to_add):

        self.chunk_grid.update_entity(self.player)
        for group in sprite_group_to_add:
            for sprite in group:
                self.chunk_grid.update_entity(sprite)

    def get_tile_by_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_cx = self.player.x - (self.main_map.scale_x * 32) // 2
        tile_cy = self.player.y - (self.main_map.scale_y * 32) // 2
        offset_x = self.player.x % 32
        offset_y = self.player.y % 32
        tx = int((mouse_x + tile_cx) // 32)
        ty = int((mouse_y + tile_cy) // 32)
        return tx, ty

    def handle_event(self, event):

        if not self.world_ready:
            return

        handled = False
        if event.type == pygame.KEYDOWN:
            if event.key == settings.KEY_INVENTORY:
                self.inventory_open = not self.inventory_open
                handled = True
            elif event.key == settings.KEY_DROP:
                if self.inventory_open and self.panel_selected_slot is not None:
                    result = self.player.inventory.drop_slot(
                        self.panel_selected_slot, 1
                    )
                else:
                    result = self.player.inventory.drop_selected(1)
                if result:
                    item, qty = result
                    drop = entity.DroppedItem(
                        self.player.x, self.player.y, item, qty, self.current_map
                    )
                    self.dropped_grp.add(drop)
                handled = True

            if event.key == settings.KEY_NPC:
                for sprite in self.entity_grp:
                    if (
                        isinstance(sprite, entity.DungeonDoor)
                        and sprite.game_map is self.current_map
                    ):
                        if sprite.player_can_enter(self.player.hitbox[0]):
                            # ENTRER dans un donjon
                            if not sprite.is_exit:
                                print(f"Entrée dans le donjon {sprite.dungeon_index}")

                                # 1) Changer de map
                                self.current_map = self.dungeon_maps[
                                    sprite.dungeon_index
                                ]
                                self.player.game_map = self.current_map

                                # 2) ALTITUDE MAP DU DONJON — OBLIGATOIRE ET IMMÉDIAT
                                self.player.altitude_map = np.zeros_like(
                                    self.current_map
                                )

                                # 3) Créer la porte de sortie si nécessaire
                                exit_door_exists = any(
                                    isinstance(e, entity.DungeonDoor)
                                    and e.is_exit
                                    and e.game_map is self.current_map
                                    for e in self.entity_grp
                                )

                                if not exit_door_exists:
                                    door_surface = pygame.Surface((32, 32))
                                    door_surface.fill((150, 75, 0))

                                    exit_door = entity.DungeonDoor(
                                        [door_surface],
                                        self.current_map,
                                        self.player.altitude_map,  # <── IMPORTANT AUSSI
                                        x=35,
                                        y=35,
                                    )
                                    exit_door.is_exit = True
                                    exit_door.exit_position = (1500, 1500)
                                    self.entity_grp.add(exit_door)

                                # 4) Positionner le joueur
                                self.player.x = 25 * 32
                                self.player.y = 25 * 32

                                # 5) Maintenant seulement : rebuild chunks
                                self.register_all_entities(
                                    [
                                        self.entity_grp,
                                        self.ennemy_grp,
                                        self.block_grp,
                                        self.npc_grp,
                                    ]
                                )

                            # SORTIR d'un donjon
                            else:
                                print(f"Sortie du donjon {sprite.dungeon_index}")
                                self.current_map = self.game_map
                                self.player.game_map = self.current_map
                                exit_x, exit_y = sprite.exit_position
                                self.player.x = exit_x * 32
                                self.player.y = exit_y * 32

                            # Rebuild chunks
                            self.register_all_entities(
                                [
                                    self.entity_grp,
                                    self.ennemy_grp,
                                    self.block_grp,
                                    self.npc_grp,
                                ]
                            )
                            break

            for sprite in self.npc_grp:
                sprite.update(self.current_map, self.player, event, self.quest_manager)

        if event.type == pygame.MOUSEBUTTONDOWN:
            tx, ty = self.get_tile_by_mouse_pos()
            if event.button == 1:  # clic droit → placer un bloc
                if not self.inventory_open:
                    self.player.inventory.try_break(
                        self.current_map, tx, ty, self.block_grp, self.player.position
                    )
                handled = True
            if event.button == 3:  # clic droit → placer un bloc
                if not self.inventory_open:
                    self.player.inventory.try_place_selected(
                        self.current_map,
                        tx,
                        ty,
                        self.block_grp,
                        self.player.position,
                        [self.entity_grp, self.ennemy_grp],
                    )
                handled = True
            if event.button == 1 and self.inventory_open:  # clic gauche inventaire
                idx = ui_inventory.get_panel_slot_at(event.pos, self.screen.get_size())
                if idx is not None:
                    self.panel_selected_slot = idx
                    if idx < self.player.inventory.hotbar_size:
                        self.player.inventory.select_hotbar(idx)
                handled = True

        if not handled and hasattr(self.player, "handle_event"):
            self.player.handle_event(event, self.joystick)
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.inventory_open
            ):
                idx = ui_inventory.get_panel_slot_at(event.pos, self.screen.get_size())
                if idx is not None:
                    self.panel_selected_slot = idx
                    if idx < self.player.inventory.hotbar_size:
                        self.player.inventory.select_hotbar(idx)
                handled = True

        index = 0
        if event.type == pygame.MOUSEWHEEL:
            self.player.inventory.scroll_hotbar(-event.y)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            item = self.player.inventory.selected_item
            if isinstance(item, items.Weapon):
                if item.on_use(self.player) != 0:
                    center = (
                        self.main_map.scale_x * 32 // 2 + 8,
                        self.main_map.scale_y * 32 // 2 + 8,
                    )
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - center[0]
                    dy = mouse_y - center[1]
                    angle = math.degrees(math.atan2(dy, -dx))
                    self.info_swipe[1] = angle
                    self.info_swipe[0] = True
                    self.info_swipe[3] = pygame.time.get_ticks()
                    nearby = self.chunk_grid.get_nearby(self.player.x, self.player.y)
                    nearby = self.chunk_grid.get_nearby(self.player.x, self.player.y)
                    for ent in nearby:
                        if ent is self.player:
                            continue
                        if not hasattr(ent, "has_life") or not ent.has_life:
                            continue
                        dist = math.hypot(self.player.x - ent.x, self.player.y - ent.y)
                        if dist > 600:
                            continue

                        tile_cx = int(self.player.x // 32)
                        tile_cy = int(self.player.y // 32)
                        offset_x = int(self.player.x % 32)
                        offset_y = int(self.player.y % 32)

                        px = ent.x - (tile_cx - self.main_map.scale_x // 2) * 32
                        py = ent.y - (tile_cy - self.main_map.scale_y // 2) * 32

                        screen_x = px + 8 - offset_x
                        screen_y = py + 8 - offset_y

                        ent_rect = pygame.Rect(
                            screen_x, screen_y, ent.hitbox_size, ent.hitbox_size
                        )
                        if ent_rect.collidepoint(pygame.mouse.get_pos()):
                            ent.life_point -= 1
                            ent.hit_flash_until = pygame.time.get_ticks() + 200
                            print("entité frappée")
                            break

        if event.type == pygame.KEYDOWN:
            for i, key in enumerate(
                [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
            ):
                if event.key == key:
                    self.player.inventory.select_hotbar(i)

        if self.joystick:
            if self.joystick.get_button(4) or self.joystick.get_button(5):
                if self.joystick.get_button(4):
                    index += 1
                if self.joystick.get_button(5):
                    index -= 1
                if index < 0:
                    index = 4
                if index > 4:
                    index = 0
                self.player.inventory.select_hotbar(index)

        for sprite in self.entity_grp:
            if isinstance(sprite, entity.DungeonDoor):
                sprite.update(self.game_map, self.player, event)

    def apply_deadzone(self, value, threshold=0.1):
        if abs(value) < threshold:
            return 0.0
        return value

    def init_quest(self):
        farmers = [n for n in self.npc_grp if isinstance(n, npc.Npc) and n.type == "fermier"]
        quest_list = [

<<<<<<< HEAD
        quest_list = [
            quest_module.Quest(
                title="Allez voir le vieux sage",
                content="Parlez au vieux npc",
                type="principale",
                objectives=[
                    quest_module.TalkObjective("Parlez au Vieux NPC", self.old_npc)
                ],
            ),
            quest_module.Quest(
                title="Aide au fermier",
                content="Le fermier a besoin d'aide, va lui parler.",
                type="principale",
                objectives=[
                    quest_module.TalkObjective("Parler au fermier", farmer_npc)
                ],
            ),
        ]
=======
        # 1) Parler au vieux sage
        quest_module.Quest(
            title="Allez voir le vieux sage",
            content="Le vieux sage souhaite vous parler.",
            type="principale",
            objectives=[
                quest_module.TalkObjective("Parlez au vieux sage", self.old_npc)
            ]
        ),

        # 2) Parler à un fermier
        quest_module.Quest(
            title="Aide au fermier",
            content="Un fermier du village a besoin d'aide.",
            type="principale",
            objectives=[
                quest_module.TalkObjective("Parler à un fermier", farmers)
            ],
            rewards=[("axe", 1)]

        ),

        # 3) Collecter du blé
        quest_module.Quest(
            title="Récolte du bois pour le fermier",
            content="Le fermier vous demande de lui rapporter 5 bois.",
            type="principale",
            objectives=[
                quest_module.CollectObjective("Collecter 5 blés", "wood", 5)
            ]
        ),

        # 4) Fabriquer une arme
        quest_module.Quest(
            title="Forger une arme",
            content="Fabriquez une arme pour vous défendre.",
            type="principale",
            objectives=[
                quest_module.CollectObjective("Obtenir une épée en bois", "wood_sword", 1)
            ]
        ),

        # 5) Tuer 3 poulets corrompus
        quest_module.Quest(
            title="Purge locale",
            content="Les poulets corrompus deviennent agressifs. Éliminez-en 3.",
            type="principale",
            objectives=[
                quest_module.KillObjective("Tuer 3 poulets corrompus", "corrupted_chicken", 3)
            ]
        ),

        # 6) Parler au garde
        #quest_module.Quest(
        #    title="Avertir le garde",
        #    content="Informez le garde de la présence de corruption.",
        #    type="principale",
        #    objectives=[
        #        quest_module.TalkObjective("Parler au garde", guard)
        #    ]
        #),
#
        # 7) Atteindre la zone corrompue
        #quest_module.Quest(
        #    title="Explorer la corruption",
        #    content="Rendez-vous près de la zone corrompue.",
        #    type="principale",
        #    objectives=[
        #        quest_module.ReachObjective("Atteindre la zone corrompue", corrupt_x, corrupt_y, radius=80)
        #    ]
        #),

        # 8) Entrer dans le donjon
        quest_module.Quest(
            title="Entrer dans le donjon",
            content="La corruption provient d'un donjon. Trouvez l'entrée.",
            type="principale",
            objectives=[
                quest_module.ReachObjective("Trouver l'entrée du donjon", 1500, 1500, radius=60)
            ]
        ),
    ]
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b

        # On ajoute ttes les quêtes dans available
        for q in quest_list:
            self.quest_manager.add_quest(q)

        # On active seulement la première au début
        self.quest_manager.accept_quest(quest_list[0])
        self.quest_init = True
        # boucle principale

    def update(self):

        self.WINDOW_SCALE = self.screen.get_width(), self.screen.get_height()

        settings.WINDOW_HEIGTH = self.WINDOW_SCALE[1]
        settings.WINDOW_WIDTH = self.WINDOW_SCALE[0]

        self.render_distance = self.WINDOW_SCALE[0]

        now = pygame.time.get_ticks()
        if self.info_swipe[0]:
            if now - self.info_swipe[3] >= self.info_swipe[2]:
                self.info_swipe[0] = False

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
        else:
            self.joystick = False

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return  # sort immédiatement
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_q
                    and pygame.key.get_mods() & pygame.KMOD_LCTRL
                ):
                    self.running = False
                    return
                if (
                    event.key == pygame.K_h
                    and pygame.key.get_mods() & pygame.KMOD_LCTRL
                ):
                    if self.main_map.show_hitbox:
                        self.main_map.show_hitbox = False
                    else:
                        self.main_map.show_hitbox = True

            if event.type == self.MUSIC_END:
                # passe à la suivante (aléatoire ou séquentielle)

                # ── séquentiel ──
                self.current_music_index = (self.current_music_index + 1) % len(
                    self.playlist
                )
                next_music = self.playlist[self.current_music_index]

                # ── ou aléatoire ──
                # next_music = random.choice(self.playlist)

                pygame.mixer.music.load(next_music)
                pygame.mixer.music.play()

            if self.sprites_initialized:
                self.handle_event(event)

        keys = pygame.key.get_pressed()

        self.screen.fill("white")
        if self.menu.in_menu:
            pygame.mixer.music.set_volume(0.2)
            if not self.music_playing:
                pygame.mixer.music.play()
                self.music_playing = True
            self.menu.draw(self.screen, self.WINDOW_SCALE)

        elif self.menu.in_settings:
            waiting_for_key = any(
                btn[1] for btn in self.settings_menu.controls.values()
            )
            self.settings_menu.draw(
                self.screen, events, self.joystick, self.WINDOW_SCALE
            )  # peut modifier button[1]
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if not waiting_for_key:  # état avant le draw
                        self.menu.in_menu = True
                        self.menu.in_settings = False
        elif not self.world_ready:
            self.loadingscreen.draw(self.screen, self.WINDOW_SCALE)

        elif self.world_ready and world_data.world_map is not None:
            if not self.sprites_initialized:
                self.init_sprites()
                self.main_map = map_render.Map(
                    self.scale_main_map,
                    self.screen,
                    [
                        self.entity_grp,
                        self.projectile_grp,
                        self.ennemy_grp,
                        self.block_grp,
                        self.plant_grp,
                        self.npc_grp,
                    ],
                )
                self.minimap = map_render.Minimap(
                    self.WINDOW_SCALE[1] - 200,
                    1000,
                    self.screen,
                    [self.entity_grp, self.ennemy_grp, self.npc_grp],
                )
                self.minimap_left_corner = map_render.Minimap(
                    240,
                    200,
                    self.screen,
                    [self.entity_grp, self.ennemy_grp, self.npc_grp],
                )

                self.main_map.build_plant_index(self.plant_grp)
                self.plant_index_built = True

                self.sprites_initialized = True
<<<<<<< HEAD
            if self.sprites_initialized and not getattr(
                self, "_chunk_registered", False
            ):
                self.register_all_entities(
                    [self.entity_grp, self.ennemy_grp, self.block_grp, self.npc_grp]
                )
=======
            if self.sprites_initialized and not getattr(self, '_chunk_registered', False):
                self.register_all_entities([self.entity_grp, self.ennemy_grp, self.block_grp, self.npc_grp, self.plant_grp])
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
                self._chunk_registered = True

            if not self.quest_init:
                self.init_quest()

            self.main_map.resize(
                int(self.screen.get_width() // 32),
                int((self.screen.get_height()) // 32),
            )

            for sprite in self.dropped_grp:
                sprite.update(self.dt, self.chunk_grid, self.current_map)

            for d in list(self.dropped_grp):
                if entity.check_box_collide(self.player.hitbox, d.hitbox):
                    self.player.inventory.add_item(d.item, d.quantity)
                    d.kill()

<<<<<<< HEAD
            self.update_chunk(
                [self.entity_grp, self.ennemy_grp, self.block_grp, self.npc_grp]
            )
=======

            self.update_chunk([self.entity_grp, self.ennemy_grp, self.block_grp, self.npc_grp, self.plant_grp])

>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b

            for sprite in self.entity_grp:
                if sprite is not self.player:
                    dist = abs(self.player.x - sprite.x) + abs(self.player.y - sprite.y)
                    if dist < self.render_distance:
                        sprite.update(self.dt, self.chunk_grid, self.current_map)

            for sprite in self.ennemy_grp:
                sprite.update(self.chunk_grid, self.current_map, self.dt)

            for sprite in self.projectile_grp:
                sprite.update(self.current_map)
                nearby = self.chunk_grid.get_nearby(sprite.x, sprite.y)
                for ent in nearby:
<<<<<<< HEAD
                    if ent is sprite:
                        continue
                    if ent is self.player:
                        continue
                    if ent is sprite.launcher:
                        continue
                    if not hasattr(ent, "hitbox"):
                        continue
=======
                    if ent is sprite: continue
                    if ent is sprite.launcher: continue
                    if not hasattr(ent, 'hitbox'): continue
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
                    if entity.check_box_collide(sprite.hitbox, ent.hitbox):
                        if hasattr(ent, "life_point"):
                            ent.life_point -= 1
                        self.chunk_grid.remove_entity(sprite)
                        sprite.kill()

                        break

            self.player.update(self.chunk_grid, self.current_map)

            if not self.inventory_open:
                self.player.input(keys, self.dt, self.joystick)

            for sprite in self.entity_grp:
                if isinstance(sprite, objects.Grotte):
                    if sprite.collides_with(self.player.hitbox):
                        self.change_map()

            self.main_map.draw(
                8,
                8,
                self.player.position,
                self.current_map,
                self.player,
                world_data.cliff_edges,
                pygame.mouse.get_pos(),
                self.player.inventory.selected_item,
                self.inventory_open,
                self.block_grp,
            )
            self.minimap_left_corner.draw(8, 8, self.player.position, self.current_map)

            self.draw_infos(20, 20, self.player.position)

            if keys[settings.KEY_MAP]:
                self.minimap.draw(
                    (self.WINDOW_SCALE[0] // 2) - ((self.WINDOW_SCALE[1] - 200) // 2),
                    10,
                    self.player.position,
                    self.game_map,
                )

            if keys[settings.KEY_MENU]:
                self.menu.in_menu = True

            interfaces.Button.update_cursor()

            if self.world_ready:
                ui_inventory.draw_hotbar(self.screen, self.player.inventory)
            if self.inventory_open:
                ui_inventory.draw_inventory_panel(
                    self.screen,
                    self.player.inventory,
                    pygame.mouse.get_pos(),
                    self.panel_selected_slot,
                )

            self.quest_manager.update(self.screen)

            if self.info_swipe[0]:
<<<<<<< HEAD
                texture_swipe_rotate = pygame.transform.rotate(
                    texture.texture_swipe_weapon[0], self.info_swipe[1] + 90
                )
                self.screen.blit(
                    texture_swipe_rotate,
                    (
                        self.main_map.scale_x * 32 // 2 + 8,
                        self.main_map.scale_y * 32 // 2 + 8,
                    ),
                )

=======
                texture_swipe_rotate = pygame.transform.rotate(texture.texture_swipe_weapon[0], self.info_swipe[1]+90)
                self.screen.blit(texture_swipe_rotate, (self.main_map.scale_x*32//2+8, self.main_map.scale_y*32//2+8))
            
            self.coeurs.draw(10, self.WINDOW_SCALE[1]-64, self.player.life_point, self.screen)
                
>>>>>>> 39d9375cb81f537a442fb71b425971ddd46b270b
            debug.draw(self.screen)
        pygame.display.flip()
        self.dt = self.clock.tick(settings.FPS) / 1000
