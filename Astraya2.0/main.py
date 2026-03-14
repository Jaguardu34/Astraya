import engine
import pygame

game_instance = engine.Game()

print("Lancement du jeu")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    game_instance.update()
pygame.quit()

