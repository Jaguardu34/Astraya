import pygame

class IntroScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 70)

        self.text = [
            "Vous vous réveillez au milieu d’une clairière...",
            "Votre tête tourne. Vous ne vous souvenez de rien.",
            "Une étrange énergie semble parcourir la forêt.",
            "Quelque chose vous observe...",
            "Une voix vous appelle au loin",
            "Une dame mystérieuse apparaît devant vous",
            "Elle vous dit : 'Bienvenue à Astraya, jeune aventurier. Tu as été choisi pour sauver ce monde de l'obscurité qui le menace.'",
            "Appuyez sur ESPACE pour continuer"
        ]

        self.index = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()
        self.letter_speed = 30
        self.current_line = ""
        self.line_done = False

    def update(self):
        now = pygame.time.get_ticks()
        if not self.line_done and now - self.last_update > self.letter_speed:
            self.last_update = now
            if len(self.current_line) < len(self.text[self.index]):
                self.current_line += self.text[self.index][len(self.current_line)]
            else:
                self.line_done = True

    def draw(self, screen):
        screen.fill("black")

        y = screen.get_height() // 3
        line_surface = self.big_font.render(self.current_line, True, "white")
        screen.blit(line_surface, (screen.get_width()//2 - line_surface.get_width()//2, y))

        if self.line_done and self.index == len(self.text)-1:
            small = self.font.render("Appuyez sur ESPACE", True, "gray")
            screen.blit(small, (screen.get_width()//2 - small.get_width()//2, y + 150))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.line_done:
                self.index += 1
                if self.index >= len(self.text):
                    self.finished = True
                else:
                    self.current_line = ""
                    self.line_done = False
