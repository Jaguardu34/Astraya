import pygame
x = 30
y= 1000


font_to_write = None
time_on_screen = 1000
last_put_on_screen = pygame.time.get_ticks()
actual_text = ""

def draw(screen):
    global last_put_on_screen, time_on_screen, actual_text
    if pygame.font.get_init():
        font_to_write = pygame.font.SysFont(None, 40)
    now = pygame.time.get_ticks()
    if now -  last_put_on_screen >  time_on_screen:
        actual_text = ""
        last_put_on_screen = now
    text_surface =  font_to_write.render( actual_text, True, "red")
    screen.blit(text_surface, (x,  y))
    

def print(text):
    global actual_text
    actual_text = text
    last_put_on_screen = pygame.time.get_ticks()