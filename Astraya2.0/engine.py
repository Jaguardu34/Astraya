import pygame
from generate_map import *
import random
import entity as ent
import texture
from settings import *
import map_render


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
        pygame.display.set_caption("Astraya 2.0")
        
        self.info_display = pygame.display.Info()
        self.WINDOW_SCALE = self.info_display.current_w - 0.1*self.info_display.current_w, self.info_display.current_h - 0.1*self.info_display.current_h
        self.screen = pygame.display.set_mode(self.WINDOW_SCALE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.dt = 0   
        self.scale_main_map = int(self.WINDOW_SCALE[0] // 32) , int(self.WINDOW_SCALE[1] // 32) - 1
        self.nbr_poulet = 100
        self.game_map = map
        self.current_map = self.game_map
        self.last_map_change = pygame.time.get_ticks()
        self.font_to_write = pygame.font.SysFont(None, 24)
        self.chunk_grid = Chunk(chunk_size=64)
        self.init_sprites()
        self.main_map = map_render.Map(self.scale_main_map, self.screen, [self.entity_grp, self.projectile_grp, self.ennemy_grp])
        self.minimap = map_render.Minimap(self.WINDOW_SCALE[1]- 200, 1000, self.screen, [self.entity_grp, self.ennemy_grp])
        self.minimap_left_corner = map_render.Minimap(240, 200, self.screen, [self.entity_grp, self.ennemy_grp])



    #creer tt les entity et les mettre dans un sprite.group
    def init_sprites(self):
        self.projectile_grp = pygame.sprite.Group()
        self.entity_grp = pygame.sprite.Group()
        self.ennemy_grp = pygame.sprite.Group()
        self.player = ent.Player(texture.texture_player, self.game_map, altitude_map, x=1500, y=1500)
        self.grotte = ent.Grotte(texture.texture_grotte, self.game_map, altitude_map, x=1520, y=1520)

        self.ennemy = ent.Ennemy(texture.texture_chicken, self.current_map, self.player, self.projectile_grp, altitude_map, 1530, 1530)

        for i in range(self.nbr_poulet):
            self.entity_grp.add(ent.Chicken(texture.texture_chicken, self.game_map, altitude_map, x=random.randint(1300, 1600), y=random.randint(1300, 1600)))
            
        self.entity_grp.add(self.player)
        self.entity_grp.add(self.grotte)
        self.ennemy_grp.add(self.ennemy)

    #changer de map 
    def change_map(self):
        change_cooldown = 2000
        now = pygame.time.get_ticks()
        if now - self.last_map_change >= change_cooldown:
            if self.current_map is self.game_map:
                self.current_map = cave
            else: self.current_map = self.game_map
            self.last_map_change = now

    #afficher les fps et coord
    def draw_infos(self, x, y, pos):
        text = self.font_to_write.render(f"Coordinates: (x: {int(pos[0])//32}, y: {int(pos[1])//32})", True, "red")
        fps = self.clock.get_fps()
        fps_text = self.font_to_write.render(f"FPS: ({fps:.2f})", True, "red")
        self.screen.blit(text, (x, y))
        self.screen.blit(fps_text, (x, y+32))

    #update les chunk aux alentours
    def update_chunk(self, sprite_group_to_add):
        self.chunk_grid.clear()
        self.chunk_grid.insert(self.player)
        for sprite_group in sprite_group_to_add:
            for sprite in sprite_group:
                self.chunk_grid.insert(sprite)
        


    #boucle principale
    def update(self):

        self.screen.fill("white")

        self.update_chunk([self.entity_grp, self.ennemy_grp])
        
        
        for sprite in self.entity_grp:
                if sprite is not self.player:
                    dist = abs(self.player.x - sprite.x) + abs(self.player.y - sprite.y)
                    if dist <   RENDER_DISTANCE:
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
            
        keys = pygame.key.get_pressed()
        self.player.input(keys, self.dt)

        for sprite in self.entity_grp:
            if isinstance(sprite, ent.Grotte):
                if sprite.collides_with(self.player.hitbox):
                    self.change_map()
                    



        
        # CHANGEMENT : Utilisation de map.cave au lieu de map.cave_biomes

        self.main_map.draw(8, 8, self.player.position, self.current_map, self.player, cliff_edges)
        self.minimap_left_corner.draw(8, 8, self.player.position, self.current_map)


        self.draw_infos(16, 16, self.player.position)


        if keys[pygame.K_TAB]:
            self.minimap.draw(0, 0, self.player.position, self.game_map)

        
        pygame.display.flip()
        self.dt = self.clock.tick(FPS) / 1000
