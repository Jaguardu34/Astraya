import pygame

# Creer une quete
class Quest():
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
        
        
    def draw(self, x, y, screen):
        width = self.font.size(self.content_sliced)[0] + self.PADDING * 2
        height = self.font.size(self.content_sliced)[1] + self.PADDING * 2
        now = pygame.time.get_ticks()
        if self.letter_index <= len(self.content):
            if now - self.last_print_interval >= self.print_interval:
                self.last_print_interval = now
                self.content_sliced = self.content[:self.letter_index]
                self.letter_index += 1
        else: self.content_sliced = self.content
        toast = pygame.Surface((width, height))
        toast.fill("white")
        pygame.draw.rect(toast, self.color, (0, 0, width, height))
        content = self.font.render(self.content_sliced, True, "black")
        toast.blit(content, (self.PADDING, self.PADDING))
        screen.blit(toast, (x-width, y))
        

class Button():
    _any_hovered = False
    def __init__(self, color, content, font_size=24, padding_width=2, padding_height=4):
        self.color = color
        self.content = content
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, self.font_size)
        self.PADDING_WIDTH = padding_width
        self.PADDING_HEIGHT = padding_height
        self.width = self.font.size(self.content)[0] + self.PADDING_WIDTH * 2
        self.height = self.font.size(self.content)[1] + self.PADDING_HEIGHT * 2
        self.x = 0
        self.y = 0
        
    def draw(self, x, y, screen):
        self.x = x
        self.y = y
        self.width = self.font.size(self.content)[0] + self.PADDING_WIDTH * 2
        self.height = self.font.size(self.content)[1] + self.PADDING_HEIGHT * 2
        button_surface = pygame.Surface((self.width, self.height))
        button_surface.fill(self.color)
        content_text = self.font.render(self.content, True, "black")
        button_surface.blit(content_text, (self.PADDING_WIDTH, self.PADDING_HEIGHT))
        screen.blit(button_surface, (self.x, self.y))

    @staticmethod
    def update_cursor():
        if Button._any_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        Button._any_hovered = False

    def is_hovered(self):
        pos_x, pos_y = pygame.mouse.get_pos()
        hovered = pos_x > self.x and pos_x < self.x + self.width and pos_y > self.y and pos_y < self.y + self.height
        if hovered:
            Button._any_hovered = True
        return hovered

    def state(self):
        click = pygame.mouse.get_pressed()
        if self.is_hovered() and click[0] == 1:
            return True
        return False
    
    
class Menu():
    def __init__(self):
        self.info_display = pygame.display.Info()
        self.WINDOW_SCALE = self.info_display.current_w, self.info_display.current_h
        self.surface = pygame.Surface(self.WINDOW_SCALE)
        
        #boutons
        self.close_btn = Button("yellow", "Fermer le jeu", 40)
        self.play_btn = Button("red", "Jouer", 40)
        self.resume_btn = Button("gray", "Reprendre", 40)
        self.buttons = {
            "close" : [self.close_btn, (self.WINDOW_SCALE[0]//2)-(self.close_btn.width//2), self.WINDOW_SCALE[1]//2+self.play_btn.height+10], 
            "play" : [self.play_btn, (self.WINDOW_SCALE[0]//2)-(self.play_btn.width//2), self.WINDOW_SCALE[1]//2]
            }
        
        self.in_menu = True
        self.launch_first_time = False
        
    def draw(self, screen):
        Button.update_cursor()
        self.surface.fill("white")
        for button in self.buttons.values():
            button[0].draw(button[1], button[2], self.surface)
        screen.blit(self.surface, (0, 0))
        
    def update(self):
        
        if self.buttons["close"][0].state():
            pygame.quit()
        if self.buttons["play"][0].state():
            self.toggle()
            if not self.launch_first_time:
                self.launch_first_time = True
                self.buttons["play"] = [self.resume_btn, (self.WINDOW_SCALE[0]//2)-(self.resume_btn.width//2), self.WINDOW_SCALE[1]//2]
            
    def toggle(self):
        if self.in_menu:
            self.in_menu = False
        else: self.in_menu = True
        
        
class LoadingScreen():
    def __init__(self):
        self.info_display = pygame.display.Info()
        self.WINDOW_SCALE = self.info_display.current_w, self.info_display.current_h
        self.surface = pygame.Surface(self.WINDOW_SCALE)
        self.font = pygame.font.SysFont(None, 100)
        self.text = "Chargement..."
        
    def draw(self, screen):
        Button.update_cursor()
        self.surface.fill("white")
        text_surface = self.font.render(self.text, True, "black")
        self.surface.blit(text_surface, (self.WINDOW_SCALE[0]//2 - (self.font.size(self.text)[0]//2), self.WINDOW_SCALE[1]//2))
        screen.blit(self.surface, (0, 0))