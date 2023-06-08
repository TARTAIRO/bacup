import pygame
import sys

# Initialisation de pygame
pygame.init()

# Définition des couleurs
NOIR = (0, 0, 0)
GRIS = (128, 128, 128)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)

# Obtenir la taille du plateau à partir des arguments de la ligne de commande
taille_plateau_str = sys.argv[1]
taille_plateau = int(taille_plateau_str.split("x")[0])

# Définition de la taille de chaque cellule en pixels
taille_cellule = 60

# Calcul de la taille de la fenêtre en fonction de la taille du plateau et de la taille des cellules
taille_fenetre = (
    taille_plateau * taille_cellule + (taille_plateau + 1) * 2, taille_plateau * taille_cellule + (taille_plateau + 1) * 2)

# Initialisation de la fenêtre
fenetre = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Plateau de jeu")

# Initialisez une matrice pour les barrières
barrieres = [[0 for _ in range(taille_plateau)] for _ in range(taille_plateau)]


class Pion:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur

    def dessiner(self):
        pygame.draw.circle(fenetre, self.couleur,
                           (self.x * taille_cellule + taille_cellule // 2 + (self.x + 1) * 2,
                            self.y * taille_cellule + taille_cellule // 2 + (self.y + 1) * 2),
                           taille_cellule // 3)

    def peut_se_deplacer_vers(self, x, y):
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        if dx > 1 or dy > 1:
            # Le pion ne peut pas se déplacer de plus d'une case
            return False
        if dx == dy:
            # Le pion ne peut pas se déplacer en diagonale
            return False
        if barrieres[self.y][self.x] == 1:
            # Il y a une barrière dans la cellule actuelle du pion
            return False
        if dx == 1:
            # Le pion se déplace horizontalement
            if self.x < x and (barrieres[y][x] == 1 or barrieres[y][x - 1] == 1):
                # Il y a une barrière à droite du pion
                return False
            if self.x > x and (barrieres[y][x] == 1 or barrieres[y][x + 1] == 1):
                # Il y a une barrière à gauche du pion
                return False
        if dy == 1:
            # Le pion se déplace verticalement
            if self.y < y and (barrieres[y][x] == 1 or barrieres[y - 1][x] == 1):
                # Il y a une barrière en bas du pion
                return False
            if self.y > y and (barrieres[y][x] == 1 or barrieres[y + 1][x] == 1):
                # Il y a une barrière en haut du pion
                return False
        return True


# Pions
pion_bleu = Pion(0, taille_plateau // 2, BLEU)
pion_rouge = Pion(taille_plateau - 1, taille_plateau // 2, ROUGE)


# Dessiner le plateau de jeu
def dessiner_plateau():
    # Effacer la fenêtre
    fenetre.fill(NOIR)

    # Dessiner les cellules
    for i in range(taille_plateau):
        for j in range(taille_plateau):
            # Calculer la position de la cellule
            cellule_x = j * taille_cellule + (j + 1) * 2
            cellule_y = i * taille_cellule + (i + 1) * 2

            # Dessiner la cellule
            pygame.draw.rect(fenetre, GRIS, (cellule_x, cellule_y, taille_cellule, taille_cellule))

    # Dessiner les pions
    pion_bleu.dessiner()
    pion_rouge.dessiner()


# Boucle principale du jeu
en_cours = True
pion_selectionne = None
while en_cours:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        # Gestion des clics de souris pour déplacer les pions
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            cellule_x, cellule_y = x // (taille_cellule + 2), y // (taille_cellule + 2)
            if pion_selectionne:
                # Si un pion est sélectionné, vérifiez si le déplacement est valide
                if pion_selectionne.peut_se_deplacer_vers(cellule_x, cellule_y):
                    pion_selectionne.x = cellule_x
                    pion_selectionne.y = cellule_y
                    pion_selectionne = None
            else:
                # Si aucun pion n'est sélectionné, vérifiez si un pion est cliqué
                if cellule_x == pion_bleu.x and cellule_y == pion_bleu.y:
                    pion_selectionne = pion_bleu
                elif cellule_x == pion_rouge.x and cellule_y == pion_rouge.y:
                    pion_selectionne = pion_rouge

    # Redessiner le plateau (avec les pions éventuellement déplacés)
    dessiner_plateau()

    # Mettre à jour la fenêtre
    pygame.display.update()

# Quitter pygame
pygame.quit()


#   cd C:\Users\hugod\Downloads\projet-main\projet-main
#   python game.py 5x5
