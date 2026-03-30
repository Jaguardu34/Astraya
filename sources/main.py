
import engine
import pygame

game_instance = engine.Game()

print("Lancement du jeu")
while game_instance.running:
    game_instance.update()
pygame.quit()

