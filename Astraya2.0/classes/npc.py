import pygame
from classes import entity
from ui import debug
import settings

class Npc(entity.Entity):
    def __init__(self, sprite, game_map, dialog_tab, altitude_map=None, x=1500, y=1500):
        super().__init__(sprite, game_map, altitude_map, x, y)
        self.dialog_tab = dialog_tab
        self.index_dialog = 0
        self.is_static = True
        self.range_action = 200
        self.close_to_player = False
        self.main_font = pygame.font.SysFont(None, 40)
        self.little_font = pygame.font.SysFont(None, 20)
        self.text_e_surface = self. main_font.render("A", True, "white")
        self.text_continue_surface = self.little_font.render("Espace", True, "black")
        self.show_on_minimap = True
        self.hitbox = [pygame.Rect(self.x+8, self.y, sprite[0].get_width()//2, sprite[0].get_height())]
        self.has_hitbox = True
        self.in_dialog = False
        self.toast = Npc_Dialog_Toast(dialog_tab[self.index_dialog])
        self.has_talk_to_player = False
        
    def draw(self, scalex, scaley, posx, posy, surface):
        super().draw(scalex, scaley, posx, posy, surface)
        if self.close_to_player:
            tile_cx = int(posx // 32)
            tile_cy = int(posy // 32)
            px = (self.x - (tile_cx - scalex//2) * 32)
            py = (self.y - (tile_cy - scaley//2) * 32)
            if 0 <= px < scalex*32 and 0 <= py < scaley*32:
                if not self.in_dialog:
                    surface.blit(self.text_e_surface, (px + (32//2-self. main_font.size("E")[0]//2), py-(self. main_font.size("E")[1]+10)))
            
            if self.in_dialog:
                if self.toast.finished_anim():
                    surface.blit(self.text_continue_surface, (px+16+(self.toast.width//2)-self.little_font.size("Espace")[0], py-40+self.toast.height))
                self.toast.content = self.dialog_tab[self.index_dialog]
                self.toast.draw(px+16-(self.toast.width//2), py-40, surface)
                if self.index_dialog == len(self.dialog_tab):
                    self.has_talk_to_player = True
                
        else:
            self.toast.reset()
            self.in_dialog = False
            self.index_dialog = 0
        
    def update(self, actual_map, player, event):
        super().update(actual_map)
        dist_x = player.x - self.x
        dist_y = player.y - self.y
        dist = (dist_x**2 + dist_y**2) ** 0.5
        
        
        if dist < self.range_action:
            self.close_to_player = True
        else: 
            self.close_to_player = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == settings.KEY_NPC:
                if not self.in_dialog:
                    self.toast.reset()
                    self.in_dialog = True
            
            if event.key == pygame.K_SPACE:
                if self.close_to_player:
                    if self.in_dialog:
                        if self.index_dialog + 1 >= len(self.dialog_tab):
                            self.toast.reset()
                            self.in_dialog = False
                            self.index_dialog = 0
                        else:
                            self.toast.reset()
                            self.index_dialog += 1

            
        
class Npc_Dialog_Toast():
    def __init__(self, content, color="white", font_size=24,):
        self.content = content
        self.color = color
        self.print_interval = 25
        self.last_print_interval = pygame.time.get_ticks()
        self.letter_index = 0
        self.content_sliced = ""
        self.PADDING = 2
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, self.font_size)
        self.width = 0
        self.height = 0
        
    def reset(self):
        self.letter_index = 0
        self.content_sliced = ""
        self.last_print_interval = pygame.time.get_ticks()
        
    def draw(self, x, y, screen):
        self.width = self.font.size(self.content_sliced)[0] + self.PADDING * 2
        self.height = self.font.size(self.content_sliced)[1] + self.PADDING * 2
        now = pygame.time.get_ticks()
        if self.letter_index <= len(self.content):
            if now - self.last_print_interval >= self.print_interval:
                self.last_print_interval = now
                self.content_sliced = self.content[:self.letter_index]
                self.letter_index += 1
        else: self.content_sliced = self.content
        toast = pygame.Surface((self.width, self.height))
        toast.fill("white")
        pygame.draw.rect(toast, self.color, (0, 0, self.width, self.height))
        content = self.font.render(self.content_sliced, True, "black")
        toast.blit(content, (self.PADDING, self.PADDING))
        screen.blit(toast, (x, y))
        
    def finished_anim(self):
        if len(self.content_sliced) == len(self.content):
            return True
        return False
    

