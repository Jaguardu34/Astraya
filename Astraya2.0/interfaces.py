import pygame

# Creer une quete
class Quest():
    def __init__(self, name, content, type_quest, color="white"):
        self.name = name
        self.content = content
        self.type = type_quest
        self.color = color
        self.print_interval = 50
        self.last_print_interval = pygame.time.get_ticks()
        self.letter_index = 0
        self.content_sliced = ""
        
        
    def render(self, x, y, screen, font):
        now = pygame.time.get_ticks()
        if self.letter_index <= len(self.content):
            if now - self.last_print_interval >= self.print_interval:
                self.last_print_interval = now
                self.content_sliced = self.content[:self.letter_index]
                self.letter_index += 1
        else: self.content_sliced = self.content
        toast = pygame.Surface((300, 100))
        toast.fill("white")
        pygame.draw.rect(toast, self.color, (0, 0, 300, 100))
        content = font.render(self.content_sliced, True, "black")
        toast.blit(content, (10, 10))
        screen.blit(toast, (x, y))
        