import pygame
import sys
from pygame import mixer
import subprocess

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

# Musique de fond
mixer.music.load("background.mp3")
mixer.music.play(0)
mixer.music.set_volume(0.2)

# Application du background
image_fond = pygame.image.load("fond.jpg")
fond = pygame.transform.scale(image_fond, TAILLE_ECRAN)

# Importation de la bannière/logo
banner = pygame.image.load("quoquo.png")
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x += 100
banner_rect.y = fenetre.get_height() // 2 - banner.get_height() // 2

# Création des boutons
largeur_bouton = 200
hauteur_bouton = 50
espacement_boutons = 10
pos_x_boutons = (TAILLE_ECRAN[0] - largeur_bouton) // 2
pos_y_bouton_jouer = (TAILLE_ECRAN[1] - (hauteur_bouton * 4 + espacement_boutons * 3)) // 2
bouton_jouer = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer, largeur_bouton, hauteur_bouton)
bouton_regles = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer + hauteur_bouton + espacement_boutons, largeur_bouton,
                            hauteur_bouton)
bouton_quitter = pygame.Rect(pos_x_boutons, pos_y_bouton_jouer + (hauteur_bouton + espacement_boutons) * 3,
                             largeur_bouton, hauteur_bouton)
bouton_retour_base = pygame.Rect(50, 50, 150, 40)

# Booléens pour indiquer l'état des fenêtres
fenetre_regles_active = False
fenetre_principale_active = True

# Règles du jeu
texte_regles = "1- But du jeu :\n\nLe but du jeu est d'être le premier joueur à atteindre le bord opposé du plateau avec son pion.\n\n2- Matériel :\n\nLe jeu Quoridor se joue sur un plateau de jeu composé de 81 cases carrées, disposées en 9x9.\nChaque joueur possède un pion de couleur distincte.\nLes joueurs disposent également d'un certain nombre de barrières (généralement 10) pour bloquer le chemin de leur adversaire.\n\n3- Déroulement du jeu :\n\nLes joueurs jouent à tour de rôle, en commençant par le joueur qui possède les pions de couleur claire.\nÀ chaque tour, un joueur peut effectuer l'une des deux actions suivantes :\n\na) Déplacer son pion : Le joueur peut déplacer son pion d'une case vers l'avant, vers l'arrière, vers la gauche ou vers la droite, mais pas en diagonale.\n\nb) Placer une barrière : Le joueur peut placer une barrière sur le plateau pour bloquer le chemin de son adversaire. Les barrières doivent être placées de manière à ne pas bloquern\n\n complètement le plateau et à ne pas enfermer un joueur.\n\n4- Règles des barrières :\n\nLes barrières sont des blocs de deux cases de longueur et doivent être placées entre deux intersections du plateau.\nLes barrières peuvent être placées verticalement ou horizontalement.\nLes barrières ne peuvent pas être déplacées une fois qu'elles ont été placées.\nLes joueurs peuvent sauter par-dessus les barrières avec leur pion.\n\n"  # 5- Règles de mouvement :\n\nLes pions peuvent se déplacer d'une case à la fois.\nLes pions ne peuvent pas sauter par-dessus les barrières.\nLes pions peuvent sauter par-dessus les pions adverses, mais pas les pions alliés.\nLes pions ne peuvent pas revenir en arrière immédiatement lors de leur tour.\n\n6- Conditions de victoire :\n\nLe premier joueur à atteindre la rangée opposée du plateau avec son pion remporte la partie.\nSi un joueur bloque complètement le passage de son adversaire avec des barrières de sorte qu'il ne puisse plus avancer, il remporte également la partie.


# Fonction pour lancer la fenêtre de jeu
def lancer_jeu():
    subprocess.call(["python", "selection.py"])


# Dans la boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if fenetre_principale_active:
                fenetre.blit(fond, (0, 0))  # Ajout de cette ligne pour réafficher l'image de fond

                # Affichage de la bannière/logo
                fenetre.blit(banner, banner_rect)

                # Affichage des boutons
                pygame.draw.rect(fenetre, NOIR, bouton_jouer)
                pygame.draw.rect(fenetre, NOIR, bouton_regles)
                pygame.draw.rect(fenetre, NOIR, bouton_quitter)

                font_bouton = pygame.font.Font(None, 32)
                text_jouer = font_bouton.render("Jouer", True, BLANC)
                text_regles = font_bouton.render("Règles", True, BLANC)
                text_quitter = font_bouton.render("Quitter", True, BLANC)

                fenetre.blit(text_jouer, (bouton_jouer.x + 50, bouton_jouer.y + 15))
                fenetre.blit(text_regles, (bouton_regles.x + 40, bouton_regles.y + 15))
                fenetre.blit(text_quitter, (bouton_quitter.x + 40, bouton_quitter.y + 15))

                if bouton_jouer.collidepoint(pos):
                    print("Bouton Jouer cliqué")
                    lancer_jeu()
                    fenetre_principale_active = False
                elif bouton_regles.collidepoint(pos):
                    print("Bouton Règles cliqué")
                    clic_son = mixer.Sound('clic.mp3')
                    clic_son.play()
                    mixer.music.stop()
                    fenetre_regles_active = True
                    fenetre_principale_active = False
                    regles_fenetre = pygame.display.set_mode(TAILLE_ECRAN, pygame.FULLSCREEN)
                    pygame.display.set_caption("Règles du jeu")
                    regles_fenetre.fill(BLANC)
                    banner_rect.x = TAILLE_ECRAN[0] + 100
                    banner_rect.y = fenetre.get_height() // 2 - banner.get_height() // 2
                elif bouton_quitter.collidepoint(pos):
                    print("Bouton Quitter cliqué")
                    pygame.quit()
                    sys.exit()

            elif fenetre_regles_active:
                if bouton_retour_base.collidepoint(pos):
                    print("Bouton Retour cliqué")
                    fenetre_principale_active = True
                    fenetre_regles_active = False
                    pygame.display.set_caption("Interface avec Pygame")  # Ajout de cette ligne

    fenetre.blit(fond, (0, 0))

    if fenetre_principale_active:
        # Affichage de la bannière/logo
        fenetre.blit(banner, banner_rect)

        # Affichage des boutons
        pygame.draw.rect(fenetre, NOIR, bouton_jouer)
        pygame.draw.rect(fenetre, NOIR, bouton_regles)
        pygame.draw.rect(fenetre, NOIR, bouton_quitter)

        font_bouton = pygame.font.Font(None, 32)
        text_jouer = font_bouton.render("Jouer", True, BLANC)
        text_regles = font_bouton.render("Règles", True, BLANC)
        text_quitter = font_bouton.render("Quitter", True, BLANC)

        fenetre.blit(text_jouer, (bouton_jouer.x + 50, bouton_jouer.y + 15))
        fenetre.blit(text_regles, (bouton_regles.x + 40, bouton_regles.y + 15))
        fenetre.blit(text_quitter, (bouton_quitter.x + 40, bouton_quitter.y + 15))

    elif fenetre_regles_active:
        regles_fenetre.blit(fond, (0, 0))
        # Affichage du texte des règles
        taille_police = 24  # Modifier la taille de la police ici
        font_regles = pygame.font.Font(None, taille_police)
        ligne_y = 50  # Position verticale initiale du texte
        for ligne in texte_regles.split("\n"):
            texte_ligne = font_regles.render(ligne, True, NOIR)
            regles_fenetre.blit(texte_ligne, (50, ligne_y))
            ligne_y += texte_ligne.get_height() + 10  # Ajout d'un décalage vertical entre les lignes

        # Affichage du bouton retour
        pygame.draw.rect(regles_fenetre, NOIR, bouton_retour_base)
        text_retour = font_bouton.render("Retour", True, BLANC)
        regles_fenetre.blit(text_retour, (bouton_retour_base.x + 50, bouton_retour_base.y + 10))

    pygame.display.flip()
