import pygame
import generate_map
import random
import entity as ent
import texture
import settings
import map_render
import threading
import render_minimap
import interfaces
import ui.ui_inventory as inventory_ui
from classes.items import get_item

class Chunk:
    def __init__(self, chunk_size=32):
        self.chunk_size = chunk_size
        self.grid = {}
        
    def get_chunk(self, x ,y):
        return (int(x // self.chunk_size), int(y // self.chunk_size))
    
    def clear(self):
        self.grid.clear()
    
    def insert(self, entity):
        chunk = self.get_chunk(entity.x, entity.y)
        if chunk not in self.grid:
            self.grid[chunk] = []
        self.grid[chunk].append(entity)
        
    def get_nearby(self, x, y):
        cx, cy = self.get_chunk(x, y)
        nearby = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                chunk = (cx +dx, cy+dy)
                if chunk in self.grid:
                    nearby.extend(self.grid[chunk])
        return nearby


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        
        self.world_ready = False
        
        #pr charger la map en arriere plan
        thread = threading.Thread(target=self._load_world)
        thread.daemon = True
        thread.start()
        
        self.info_display = pygame.display.Info()
        self.WINDOW_SCALE = self.info_display.current_w, self.info_display.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.dt = 0   
        self.scale_main_map = int(self.WINDOW_SCALE[0] // 32) , int((self.WINDOW_SCALE[1] - 200) // 32)
        self.render_distance = self.WINDOW_SCALE[0]//2
        
        self.game_map = None
        self.current_map = None
        
        self.last_map_change = pygame.time.get_ticks()
        self.font_to_write = pygame.font.SysFont(None, 24)
        self.chunk_grid = Chunk(chunk_size=64)
        self.in_menu = False
        self.quest = interfaces.Quest("ceci est une quete de test tres tres longue pour voir si ca tient dans ce tout petit carré", "red", 30)
        
        #interface
        self.menu = interfaces.MainMenu()
        self.loadingscreen = interfaces.LoadingScreen()
        self.settings_menu = interfaces.SettingsMenu()
        
        #inventaire 
        self.inventory_open = False
        self.panel_selected_slot = None

    #charger la map gigantesque de Pau en arriere plan
    def _load_world(self):
        result = generate_map.map_generate()
        generate_map.map, generate_map.texture_variants, generate_map.cave, \
        generate_map.coord_vil, generate_map.coord_grottes, generate_map.altitude_map, \
        generate_map.cliff_edges, generate_map.villages = result
        
        render_minimap.generate_minimap()
        
        self.game_map = generate_map.map
        self.current_map = self.game_map
        

        self.init_sprites()
        self.main_map = map_render.Map(self.scale_main_map, self.screen, [self.entity_grp, self.projectile_grp, self.ennemy_grp])
        self.minimap = map_render.Minimap(self.WINDOW_SCALE[1] - 200, 1000, self.screen, [self.entity_grp, self.ennemy_grp])
        self.minimap_left_corner = map_render.Minimap(240, 200, self.screen, [self.entity_grp, self.ennemy_grp])
        
        self.world_ready = True

    #creer tt les entity et les mettre dans un sprite.group
    def init_sprites(self):
        self.projectile_grp = pygame.sprite.Group()
        self.entity_grp = pygame.sprite.Group()
        self.ennemy_grp = pygame.sprite.Group()
        
        alt = generate_map.altitude_map  # raccourci
        
        self.player = ent.Player(texture.texture_player, self.game_map, alt, x=1500, y=1500)
        self.grotte = ent.Grotte(texture.texture_grotte, self.game_map, alt, x=1520, y=1520)
        self.ennemy = ent.Ennemy(texture.texture_chicken, self.current_map, self.player, self.projectile_grp, alt, 1530, 1530)

        for i in range(100):
            self.entity_grp.add(ent.Chicken(texture.texture_chicken, self.game_map, alt, x=random.randint(1300, 1600), y=random.randint(1300, 1600)))
            
        self.entity_grp.add(self.player)
        self.entity_grp.add(self.grotte)
        self.ennemy_grp.add(self.ennemy)

    #changer de map 
    def change_map(self):
        import generate_map
        change_cooldown = 2000
        now = pygame.time.get_ticks()
        if now - self.last_map_change >= change_cooldown:
            if self.current_map is self.game_map:
                self.current_map = generate_map.cave
            else:
                self.current_map = self.game_map
            self.last_map_change = now

    #afficher les fps et coord
    def draw_infos(self, x, y, pos):
        fps = self.clock.get_fps()
        text = self.font_to_write.render(f"Coordinates: (x: {int(pos[0])//32}, y: {int(pos[1])//32})", True, "red")
        text_fps = self.font_to_write.render(f"FPS : {fps:.2f}", True, "red")
        pygame.display.set_caption(
            f"Astraya 2.0 - FPS : {fps:.2f}","Astraya")
        self.screen.blit(text, (x, y))
        self.screen.blit(text_fps, (x, y+self.font_to_write.size("A")[1]+2))


    #update les chunk aux alentours
    def update_chunk(self, sprite_group_to_add):
        self.chunk_grid.clear()
        self.chunk_grid.insert(self.player)
        for sprite_group in sprite_group_to_add:
            for sprite in sprite_group:
                self.chunk_grid.insert(sprite)
                

    def handle_event(self, event):
        """Handle inventory toggle, drop, place; forward rest to player."""
        handled = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.inventory_open = not self.inventory_open
                handled = True
            elif event.key == pygame.K_q:
                if self.inventory_open and self.panel_selected_slot is not None:
                    result = self.player.inventory.drop_slot(self.panel_selected_slot, 1)
                else:
                    result = self.player.inventory.drop_selected(1)
                if result:
                    item, qty = result
                    drop = ent.DroppedItem(
                        self.player.x, self.player.y, item, qty, self.current_map
                    )
                    self.dropped_grp.add(drop)
                handled = True
            elif event.key == pygame.K_r:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                tx = int(mouse_x // 32)
                ty = int(mouse_y // 32)
                
                self.player.inventory.try_place_selected(
                    self.current_map, tx, ty, 2
                )
                handled = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.inventory_open:
            idx = inventory_ui.get_panel_slot_at(event.pos, self.screen.get_size())
            if idx is not None:
                self.panel_selected_slot = idx
                if idx < self.player.inventory.hotbar_size:
                    self.player.inventory.select_hotbar(idx)
            handled = True
        if not handled and hasattr(self.player, "handle_event"):
            self.player.handle_event(event)

    #boucle principale
    def update(self):
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL and event.key == pygame.K_q:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                self.handle_event(event)

        keys = pygame.key.get_pressed()
        self.screen.fill("white")
        if self.menu.in_menu:
            self.menu.draw(self.screen)
            
        
        elif self.menu.in_settings:
            waiting_for_key = any(btn[1] for btn in self.settings_menu.controls.values())
            self.settings_menu.draw(self.screen, events)  # peut modifier button[1]
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if not waiting_for_key:  # état avant le draw
                        self.menu.in_menu = True
                        self.menu.in_settings = False
        elif not self.world_ready:
            self.loadingscreen.draw(self.screen)
            
        else :

            #securite pr eviter enorme mega giga crash
            if not self.world_ready:
                return
            
            self.update_chunk([self.entity_grp, self.ennemy_grp])
            
            
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
                for entity in nearby:
                    if entity is sprite: continue
                    if entity is self.player: continue
                    if entity is sprite.launcher: continue
                    if not hasattr(entity, 'hitbox'): continue
                    if ent.check_box_collide(sprite.hitbox, entity.hitbox):
                        if hasattr(entity, 'life_point'):
                            entity.life_point -= 1
                        sprite.kill()
                        break

            
            self.player.update(self.chunk_grid, self.current_map)
                
            
            self.player.input(keys, self.dt)

            for sprite in self.entity_grp:
                if isinstance(sprite, ent.Grotte):
                    if sprite.collides_with(self.player.hitbox):
                        self.change_map()
            
            # CHANGEMENT : Utilisation de map.cave au lieu de map.cave_biomes

            self.main_map.draw(8, 8, self.player.position, self.current_map, self.player, generate_map.cliff_edges)
            self.minimap_left_corner.draw(8, 8, self.player.position, self.current_map)


            self.draw_infos(16, 16, self.player.position)
            
            self.quest.draw(self.WINDOW_SCALE[0] - 10, 10, self.screen)


            if keys[settings.KEY_MAP]:
                self.minimap.draw((self.WINDOW_SCALE[0]//2) - ((self.WINDOW_SCALE[1] - 200) //2), 10, self.player.position, self.game_map)


            if keys[settings.KEY_MENU]:
                self.menu.in_menu = True
            
            interfaces.Button.update_cursor()
            
        inventory_ui.draw_hotbar(self.screen, self.player.inventory)
        if self.inventory_open:
            inventory_ui.draw_inventory_panel(
                self.screen, self.player.inventory, pygame.mouse.get_pos(),
                self.panel_selected_slot,
            )
            
            
            
        
        pygame.display.flip()
        self.dt = self.clock.tick(settings.FPS) / 1000
