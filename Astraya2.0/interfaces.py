import pygame
import settings

# Creer une quete
class Quest_PopUp():
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
        self._pressing = False
        
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
            if not self._pressing:  # premier frame seulement
                self._pressing = True
                return True
        else:
            self._pressing = False
        return False
    
class FullscreenMenu():
    def __init__(self):
        self.info_display = pygame.display.Info()
        self.WINDOW_SCALE = self.info_display.current_w, self.info_display.current_h
        self.surface = pygame.Surface(self.WINDOW_SCALE)
    
    def draw(self, window_scale):
        self.WINDOW_SCALE = window_scale
        self.surface = pygame.Surface(self.WINDOW_SCALE)
    
class MainMenu(FullscreenMenu):
    def __init__(self):
        super().__init__()
        
        #boutons
        self.close_btn = Button("yellow", "Fermer le jeu", 40)
        self.play_btn = Button("red", "Jouer", 40)
        self.resume_btn = Button("gray", "Reprendre", 40)
        self.settings_btn = Button("gray", "Parametres", 40)
        self.buttons = {
            "play" : [self.play_btn, (self.WINDOW_SCALE[0]//2)-(self.play_btn.width//2), self.WINDOW_SCALE[1]//2],
            "close" : [self.close_btn, 10, 10], 
            "settings" : [self.settings_btn, (self.WINDOW_SCALE[0]//2)-(self.settings_btn.width//2), self.WINDOW_SCALE[1]//2+self.play_btn.height+10]
            }
        
        self.in_menu = True
        self.launch_first_time = False
        self.in_settings= False
        
    def draw(self, screen, window_scale):
        super().draw(window_scale)
        self.buttons = {
            "play" : [self.play_btn, (self.WINDOW_SCALE[0]//2)-(self.play_btn.width//2), self.WINDOW_SCALE[1]//2],
            "close" : [self.close_btn, 10, 10], 
            "settings" : [self.settings_btn, (self.WINDOW_SCALE[0]//2)-(self.settings_btn.width//2), self.WINDOW_SCALE[1]//2+self.play_btn.height+10]
            }
        
        self.surface.fill("white")
        for button in self.buttons.values():
            button[0].draw(button[1], button[2], self.surface)
        screen.blit(self.surface, (0, 0))
        Button.update_cursor()
        self.update()
        
    def update(self):
        
        if self.buttons["close"][0].state():
            pygame.quit()
        if self.buttons["play"][0].state():
            self.in_menu = False
            if not self.launch_first_time:
                self.launch_first_time = True
                self.buttons["play"] = [self.resume_btn, (self.WINDOW_SCALE[0]//2)-(self.resume_btn.width//2), self.WINDOW_SCALE[1]//2]
        if self.buttons["settings"][0].state():
            self.in_menu = False
            self.in_settings = True

        
        
        
class LoadingScreen(FullscreenMenu):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 100)
        self.text = "Chargement..."
        
    def draw(self, screen, window_scale):
        super().draw(window_scale)
        self.surface.fill("white")
        text_surface = self.font.render(self.text, True, "black")   
        self.surface.blit(text_surface, (self.WINDOW_SCALE[0]//2 - (self.font.size(self.text)[0]//2), self.WINDOW_SCALE[1]//2))
        screen.blit(self.surface, (0, 0))
        Button.update_cursor()
        
class SettingsMenu(FullscreenMenu):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 40)
        self.controls = {
            "Monter" : [Button("lightgray", "...", 40), False, settings.KEY_UP],
            "Descendre" : [Button("lightgray", "...", 40), False, settings.KEY_DOWN],
            "Gauche" : [Button("lightgray", "...", 40), False, settings.KEY_LEFT],
            "Droite" : [Button("lightgray", "...", 40), False, settings.KEY_RIGHT],
            "Map" : [Button("lightgray", "...", 40), False, settings.KEY_MAP],
            "Menu" : [Button("lightgray", "...", 40), False, settings.KEY_MENU],
            "Inventaire" : [Button("lightgray", "...", 40), False, settings.KEY_INVENTORY],
            "Drop" : [Button("lightgray", "...", 40), False, settings.KEY_DROP]
        }

            
            
            
        
        self.button_fps = [
            (Button("gray", "30", 40), 30),
            (Button("gray", "60", 40), 60),
            (Button("gray", "120", 40), 120),
            (Button("gray", "240", 40), 240)
        ]
        
        self.display_modes = pygame.display.list_modes()
        
        self.tab_display_button = []
        for i in range(len(self.display_modes)):
            self.tab_display_button.append(Button("gray", f"{str(self.display_modes[i][0])}, {str(self.display_modes[i][1])}"))
            
            
            
        
        self.event = None
    
    def draw(self, screen, event, joystick_plugged, window_scale):
        super().draw(window_scale)
        self.event = event
        text_surface=""
        self.surface.fill("white")
        x = 0
        for control in self.controls:
            self.controls[control][0].draw(300, self.WINDOW_SCALE[1]//2+x*50, self.surface)
            text_surface = self.font.render(control, True, "black")
            self.surface.blit(text_surface, (100, self.WINDOW_SCALE[1]//2+x*50))
            x+=1
        
            
        for i in range(len(self.button_fps)):
            self.button_fps[i][0].draw(200+i*80, self.WINDOW_SCALE[1]//2-200, self.surface)
            
        for i in range(len(self.tab_display_button)):
            self.tab_display_button[i].draw(self.WINDOW_SCALE[0]-400, 10+i*30, self.surface)
        
        fps_text = "FPS :"
        text_fps_surface = self.font.render(fps_text, True, "black")
        self.surface.blit(text_fps_surface, (100, self.WINDOW_SCALE[1]//2-200))
        
        joystick_text_surface = ""
        if joystick_plugged:
            joystick_text_surface = self.font.render("Manette Branchée", True, "orange")
        else: joystick_text_surface = self.font.render("Manette Débranchée", True, "gray")

        
        self.surface.blit(joystick_text_surface, (self.WINDOW_SCALE[1]- 500, self.WINDOW_SCALE[1]//2))
        
        
        
        screen.blit(self.surface, (0, 0))
        Button.update_cursor()
        
        self.update()
        
    def update(self):
        for button in self.button_fps:
            if settings.FPS == button[1]:
                button[0].color = "dodgerblue"
            else:   
                button[0].color = "lightgray"

            if button[0].state():
                settings.FPS = button[1]

        settings_map = {
            "Monter": "KEY_UP",
            "Descendre": "KEY_DOWN",
            "Gauche": "KEY_LEFT",
            "Droite": "KEY_RIGHT",
            "Map": "KEY_MAP",
            "Menu": "KEY_MENU",
            "Inventaire" : "KEY_INVENTORY",
            "Drop" : "KEY_DROP"
        }

        for key_name, button in self.controls.items():  # items() pas values() !
            if button[1]:
                button[0].color = "red"
                button[0].content = "Appuyez sur une touche..."
               
                for event in self.event:
                    if event.type == pygame.KEYDOWN:
                        button[1] = False
                        button[2] = event.key
                        setattr(settings, settings_map[key_name], event.key)  # ← manquait
            else:
                button[0].color = "lightgray"
                button[0].content = pygame.key.name(button[2])

            if button[0].state():
                if not button[1]:
                    button[1] = True
        
    
    
            
        
