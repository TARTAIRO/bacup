import pygame
import subprocess

# Initialise pygame
pygame.init()

# Initialise la fenetre pygame
TAILLE_ECRAN = (1920, 1080)
fenetre = pygame.display.set_mode(TAILLE_ECRAN, pygame.FULLSCREEN)
pygame.display.set_caption("Choose the size of the game board")

# Défini les différentes tailles de plateau de jeu
board_sizes = ["5x5", "7x7", "9x9", "11x11"]

# Configure la police d'écriture
font = pygame.font.SysFont(None, 30)

# Crée un text object pour chaque taille de plateau de jeu
text_objects = [font.render(size, True, (255, 255, 255)) for size in board_sizes]

# Calcule la position de chaque text sur la fenetre
text_positions = [(TAILLE_ECRAN[0]//2 - text.get_width()//2, TAILLE_ECRAN[1]//2 - text.get_height()//2 + 100*i) for i, text in enumerate(text_objects)]

#Boucle pygame
clock = pygame.time.Clock()

# Ouvre la fenêtre de selection
running = True
while running:
    # events pygame 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # prends la position du curseur de la souris
            x, y = pygame.mouse.get_pos()
            
            # Check si le click est sur un texte correspondant à la taille du plateau de jeu
            for i, pos in enumerate(text_positions):
                if pos[0] <= x <= pos[0] + text_objects[i].get_width() and pos[1] <= y <= pos[1] + text_objects[i].get_height():
                    # Exécute le fichier "game.py" avec la taille choisie comme argument et ferme la fenêtre
                    subprocess.call(["python", "game.py", board_sizes[i]])
                    running = False
                    
    
    # Nettoie la fenêtre pygame
    fenetre.fill((0, 0, 0))
    
    # Affiche les text objects
    for i, text in enumerate(text_objects):
        fenetre.blit(text, text_positions[i])
    
    # Update la fenêtre pygame
    pygame.display.update()

# Quitte la fenêtre pygame
pygame.quit() 
