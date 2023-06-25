import pygame  # Importation du module Pygame pour l'interface graphique
import sys  # Importation du module sys pour récupérer les données choisies par l'utilisateur sur la page précédente

# Initialisation de pygame
pygame.font.init()
font = pygame.font.SysFont(None, 24)  # Choisissez la taille et le style de la police


class Parametres:  # Classe comportant les différents paramètres pour le Jeu
    # Définition des couleurs
    NOIR = (0, 0, 0)
    GRIS = (128, 128, 128)
    BLEU = (0, 0, 255)
    ROUGE = (255, 0, 0)
    JAUNE = (255, 255, 0)
    VERT = (0, 255, 0)
    BLANC = (255, 255, 255)

    # Obtenir la taille du plateau et le nombre de joueurs à partir des sélections de l'utilisateur via la page selection.py
    taille_plateau_str = sys.argv[1]
    taille_plateau = int(taille_plateau_str.split("x")[0])
    nb_players = int(sys.argv[2])

    # Définition de la taille de chaque cellule en pixels
    taille_cellule = 60

    # Calcul de la taille de la fenêtre en fonction de la taille du plateau, de la taille des cellules et du menu
    taille_fenetre = (taille_plateau * taille_cellule + (taille_plateau + 1) * 2 + 200,
                      taille_plateau * taille_cellule + (taille_plateau + 1) * 2)

    # Initialisation de la fenêtre
    fenetre = pygame.display.set_mode(taille_fenetre)


class Pion:  # Classe comportant tous les méthodes et fonctions relatives aux Pions

    def __init__(self, x, y, couleur):  # Initialisation des paramètres des pions
        self.x = x
        self.y = y
        self.couleur = couleur

    def dessiner(self):  # Fonction qui permet de dessiner les pions ou les redessiner en cas de déplacement
        c = Parametres.taille_cellule  # Importer la taille de la cellule depuis la classe Parametres
        pygame.draw.circle(Parametres.fenetre, self.couleur,
                           (self.x * c + c // 2 + (self.x + 1) * 2, self.y * c + c // 2 + (self.y + 1) * 2),
                           c // 3)  # Dessine un cercle qui représente le Pion

    def peut_se_deplacer_vers(self, x, y):
        c = Parametres.taille_cellule  # Importer la taille de la cellule depuis la classe Parametres
        dx = x - self.x
        dy = y - self.y
        if abs(dx) > 1 or abs(dy) > 1:  # Le joueur ne peut se déplacer que d'une case
            return False
        if abs(dx) == abs(dy):  # Le joueur ne peut se déplacer en diagonale
            for joueur in joueurs:
                if joueur.pion.x == x and joueur.pion.y == y:  # Le joueur ne peut pas poser son pions sur celui d'un autre joueur
                    return False
        for joueur in joueurs:
            if joueur.pion.x == x and joueur.pion.y == y:
                return False
        for barriere in Barriere.barrieres:  # Le joueur ne peut pas traverser les barrières
            if barriere.orientation == "vertical":
                if dy == 0:
                    if (self.x == barriere.x - 1 and dx == 1) or (self.x == barriere.x + 1 and dx == -1):
                        if abs(self.y * c + c / 2 + (self.y + 1) * 2 - (barriere.y * c + (barriere.y + 1) * 2)) < c:
                            return False
            elif barriere.orientation == "horizontal":
                if dx == 0:
                    if (self.y == barriere.y - 1 and dy == 1) or (self.y == barriere.y + 1 and dy == -1):
                        if abs(self.x * c + c / 2 + (self.x + 1) * 2 - (barriere.x * c + (barriere.x + 1) * 2)) < c:
                            return False
        return True


# Placement des Pions au début du jeu
tp = Parametres.taille_plateau  # Importer la taille du plateau depuis la classe Parametres
# Définition des paramètres de chaque pion
pion_bleu = Pion(0, tp // 2, Parametres.BLEU)
pion_rouge = Pion(tp - 1, tp // 2, Parametres.ROUGE)
pion_jaune = Pion(tp // 2, 0, Parametres.JAUNE)
pion_vert = Pion(tp // 2, tp - 1, Parametres.VERT)


class Barriere:
    nombre_max_barriere = 10  # Remplacez par la valeur souhaitée
    barrieres = []  # Liste pour stocker les instances de barrières

    def __init__(self, ligne, colonne, orientation, couleur):
        self.ligne = ligne
        self.colonne = colonne
        self.orientation = orientation
        self.couleur = couleur
        Barriere.barrieres.append(self)

    def dessiner(self):
        c = Parametres.taille_cellule
        if self.orientation == 'horizontale':
            x1 = self.colonne * c + c // 2
            y1 = self.ligne * c + c // 4
            x2 = x1 + c
            y2 = y1
        else:  # orientation verticale
            x1 = self.colonne * c + c // 4
            y1 = self.ligne * c + c // 2
            x2 = x1
            y2 = y1 + c

        pygame.draw.line(Parametres.fenetre, self.couleur, (x1, y1), (x2, y2), 5)


# Classe joueur pour stocker des informations sur chaque joueur
class Joueur:
    def __init__(self, pion, barrieres_restantes, couleur, couleur_nom):  # Initialisation des paramètres des Pions
        self.pion = pion
        self.barrieres_restantes = barrieres_restantes
        self.couleur = couleur  # Ajoutez un attribut de couleur
        self.couleur_nom = couleur_nom  # Ajoutez un attribut pour le nom de la couleur


# Calculer le nombre de barrières que chaque joueur doit recevoir
barrieres_par_joueur = Barriere.nombre_max_barriere // Parametres.nb_players

# Création des objets Joueurs avec le nombre de barrières attribué
joueur_bleu = Joueur(pion_bleu, barrieres_par_joueur, Parametres.BLEU, "Bleu")
joueur_rouge = Joueur(pion_rouge, barrieres_par_joueur, Parametres.ROUGE, "Rouge")
joueur_jaune = Joueur(pion_jaune, barrieres_par_joueur, Parametres.JAUNE,
                      "Jaune") if Parametres.nb_players == 4 else None
joueur_vert = Joueur(pion_vert, barrieres_par_joueur, Parametres.VERT, "Vert") if Parametres.nb_players == 4 else None

# Liste des joueurs actifs
joueurs = [joueur_bleu, joueur_rouge]
if Parametres.nb_players == 4:
    joueurs.extend([joueur_jaune, joueur_vert])

# Définir le joueur en cours
joueur_en_cours = 0


class Jeu:  # Classe comportant tous les méthodes et fonctions relatives au Jeu
    def dessiner_plateau():  # Dessiner le plateau de jeu
        Parametres.fenetre.fill(Parametres.NOIR)  # Effacement de la fenêtre
        c = Parametres.taille_cellule  # Importer la taille de la cellule depuis la classe Parametres
        for i in range(Parametres.taille_plateau):  # Dessiner les cellules

            for j in range(Parametres.taille_plateau):
                # Calculer la position de chaque cellule
                cellule_x = j * c + (j + 1) * 2
                cellule_y = i * c + (i + 1) * 2

                # Dessiner la cellule
                pygame.draw.rect(Parametres.fenetre, Parametres.GRIS, (cellule_x, cellule_y, c, c))
        # Dessiner les pions en fonction du nombre de joueurs
        pion_bleu.dessiner()
        pion_rouge.dessiner()
        if Parametres.nb_players == 4:  # Si l'utilisateur a sélectionné 4 joueurs alors on rajoute deux pions supplémentaires
            pion_jaune.dessiner()
            pion_vert.dessiner()
        # Dessiner le menu de droite
        pygame.draw.rect(Parametres.fenetre, Parametres.GRIS,
                         (Parametres.taille_fenetre[0] - 200, 0, 200, Parametres.taille_fenetre[1]))

    def effacer_fenetre():
        Parametres.fenetre.fill(Parametres.NOIR)

    en_cours = True  # Défini si le jeu est encore en cours ou non
    c = Parametres.taille_cellule  # Importer la taille de la cellule depuis la classe Parametres
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si la fenêtre est quittée, arrêter la boucle
                en_cours = False
                # Autres codes...
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                cellule_x, cellule_y = x // (c + 2), y // (c + 2)
                # Si un pion est sélectionné
                if joueurs[joueur_en_cours].pion.peut_se_deplacer_vers(cellule_x,
                                                                       cellule_y):  # Vérifie le déplacement du joueur
                    joueurs[joueur_en_cours].pion.x = cellule_x
                    joueurs[joueur_en_cours].pion.y = cellule_y
                    # Changer de tour
                    joueur_en_cours = (joueur_en_cours + 1) % len(joueurs)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # Si le joueur a encore des barrières à poser
                if joueurs[joueur_en_cours].barrieres_restantes > 0:
                    x, y = event.pos
                    cellule_x, cellule_y = x // (c + 2), y // (c + 2)
                    if len(Barriere.barrieres) < Barriere.nombre_max_barriere:
                        if abs(x - (cellule_x * (c + 2) + c / 2)) > abs(y - (cellule_y * (c + 2) + c / 2)):
                            orientation = "vertical"
                        else:
                            orientation = "horizontal"
                        nouvelle_barriere = Barriere(cellule_x, cellule_y, orientation,
                                                     joueurs[joueur_en_cours].couleur)
                        Barriere.barrieres.append(nouvelle_barriere)
                        # Réduire le nombre de barrières restantes pour le joueur
                        joueurs[joueur_en_cours].barrieres_restantes -= 1
                        # Changer de tour
                        joueur_en_cours = (joueur_en_cours + 1) % len(joueurs)

        # Redessiner le plateau (avec les pions éventuellement déplacés)
        dessiner_plateau()
        for barriere in Barriere.barrieres:
            barriere.dessiner()

        # Mise à jour du tour du joueur dans le menu de droite
        pygame.draw.rect(Parametres.fenetre, Parametres.GRIS,
                         (Parametres.taille_fenetre[0] - 200, 0, 200, Parametres.taille_fenetre[1]))
        text = font.render("Tour du Joueur " + joueurs[joueur_en_cours].couleur_nom, True, Parametres.NOIR)
        Parametres.fenetre.blit(text, (Parametres.taille_fenetre[0] - 190, 10))
        # Mise à jour du nombre de barrières restantes au joueur dans le menu de droite
        text_barrieres = font.render("Barrières restantes : " + str(joueurs[joueur_en_cours].barrieres_restantes), True,
                                     Parametres.NOIR)
        Parametres.fenetre.blit(text_barrieres, (Parametres.taille_fenetre[0] - 190, 40))

        # Vérification de la victoire
        for joueur in joueurs:
            victoire_texte = font.render(
                "Bravo joueur " + joueurs[joueur_en_cours - 1].couleur_nom + ", vous avez gagné !", True,
                joueurs[joueur_en_cours - 1].couleur)
            if joueur.pion.x == Parametres.taille_plateau - 1 and joueur.couleur == Parametres.BLEU:
                effacer_fenetre()
                Parametres.fenetre.blit(victoire_texte, (50, 200))
            elif joueur.pion.x == 0 and joueur.couleur == Parametres.ROUGE:
                effacer_fenetre()
                Parametres.fenetre.blit(victoire_texte, (50, 200))
            elif joueur.pion.y == Parametres.taille_plateau - 1 and joueur.couleur == Parametres.JAUNE:
                effacer_fenetre()
                Parametres.fenetre.blit(victoire_texte, (50, 200))
            elif joueur.pion.y == 0 and joueur.couleur == Parametres.VERT:
                effacer_fenetre()
                Parametres.fenetre.blit(victoire_texte, (50, 200))

        # Mettre à jour la fenêtre
        pygame.display.update()
