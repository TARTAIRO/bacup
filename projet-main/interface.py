import pygame
import sys
import subprocess
from network import Network


# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Définition de la taille de l'écran
TAILLE_ECRAN = (1920, 1080)

# Création de la fenêtre en plein écran
fenetre = pygame.display.set_mode(TAILLE_ECRAN, pygame.FULLSCREEN)
pygame.display.set_caption("Interface avec Pygame")

# Application du background
#background = pygame.image.load('space.jpg')
#background.convert()
#running = True
#while running:
    #fenetre.blit(background, (0, 0))
    #pygame.display.flip()


# Création des boutons
largeur_bouton = 200
hauteur_bouton = 50
espacement_boutons = 10
pos_x_boutons = (TAILLE_ECRAN[0] - largeur_bouton) // 2
pos_y_bouton_jouer = (TAILLE_ECRAN[1] - (hauteur_bouton * 4 + espacement_boutons * 3)) // 2
bouton_jouer = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer, largeur_bouton, hauteur_bouton)
bouton_regles = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer + hauteur_bouton + espacement_boutons, largeur_bouton, hauteur_bouton)
bouton_parametres = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer + (hauteur_bouton + espacement_boutons) * 2, largeur_bouton, hauteur_bouton)
bouton_quitter = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer + (hauteur_bouton + espacement_boutons) * 3, largeur_bouton, hauteur_bouton)


# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Récupération des coordonnées du clic
            pos = pygame.mouse.get_pos()

            # Vérification du clic sur les boutons
            if bouton_jouer.collidepoint(pos):
                print("Bouton Jouer cliqué")
                # Ajouter ici la fonctionnalité souhaitée pour le bouton "Jouer"
                jouer_fenetre = pygame.display.set_mode((800, 600))
                subprocess.call(["python", "selection.py"])
                pygame.quit()
                sys.exit()
            elif bouton_regles.collidepoint(pos):
                print("Bouton Règles cliqué")
                # Ajouter ici la fonctionnalité souhaitée pour le bouton "Règles"
                regles_fenetre = pygame.display.set_mode((800, 600))
                pygame.display.set_caption("Règles du jeu")
                regles_fenetre.fill(BLANC)
                # Ajouter ici le code pour afficher les règles du jeu dans la nouvelle fenêtre
                pygame.display.flip()
            elif bouton_parametres.collidepoint(pos):
                print("Bouton Paramètres cliqué")
                # Ajouter ici la fonctionnalité souhaitée pour le bouton "Paramètres"
                parametre_fenetre = pygame.display.set_mode((800, 600))
                pygame.display.set_caption("Paramètres du jeu")
                parametre_fenetre.fill(BLANC)
                # Ajouter ici le code pour afficher les paramètres du jeu dans la nouvelle fenêtre
                pygame.display.flip()
            elif bouton_quitter.collidepoint(pos):
                print("Bouton Quitter cliqué")
                pygame.quit()
                sys.exit()

    # Effacement de l'écran
    fenetre.fill(BLANC)

    # Dessin des boutons
    pygame.draw.rect(fenetre, NOIR, bouton_jouer)
    pygame.draw.rect(fenetre, NOIR, bouton_regles)
    pygame.draw.rect(fenetre, NOIR, bouton_parametres)
    pygame.draw.rect(fenetre, NOIR, bouton_quitter)

    # Ajout du texte sur les boutons
    font = pygame.font.Font(None, 36)
    text_jouer = font.render("Jouer", True, BLANC)
    text_regles = font.render("Règles", True, BLANC)
    text_parametres = font.render("Paramètres", True, BLANC)
    text_quitter = font.render("Quitter", True, BLANC)

    fenetre.blit(text_jouer, (pos_x_boutons + largeur_bouton // 2 - text_jouer.get_width() // 2, pos_y_bouton_jouer + hauteur_bouton // 2 - text_jouer.get_height() // 2))
    fenetre.blit(text_regles, (pos_x_boutons + largeur_bouton // 2 - text_regles.get_width() // 2, pos_y_bouton_jouer + hauteur_bouton + espacement_boutons + hauteur_bouton // 2 - text_regles.get_height() // 2))
    fenetre.blit(text_parametres, (pos_x_boutons + largeur_bouton // 2 - text_parametres.get_width() // 2, pos_y_bouton_jouer + (hauteur_bouton + espacement_boutons) * 2 + hauteur_bouton // 2 - text_parametres.get_height() // 2))
    fenetre.blit(text_quitter, (pos_x_boutons + largeur_bouton // 2 - text_quitter.get_width() // 2, pos_y_bouton_jouer + (hauteur_bouton + espacement_boutons) * 3 + hauteur_bouton // 2 - text_quitter.get_height() // 2))

    # Mise à jour de l'affichage
    pygame.display.flip()
