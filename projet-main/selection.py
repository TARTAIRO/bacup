import pygame
import subprocess
import sys

# Initialise pygame
pygame.init()

# Initialise la fenetre pygame
TAILLE_ECRAN = (1920, 1080)
fenetre = pygame.display.set_mode(TAILLE_ECRAN)
pygame.display.set_caption("Choisissez la taille du plateau, le nombre de joueurs et le nombre de barrières")

# Défini les différentes tailles de plateau de jeu, le nombre de joueurs et le nombre de barrières
board_sizes = ["5x5", "7x7", "9x9", "11x11"]
num_players = ["2", "4"]
num_barriers = list(range(4, 41, 4))  # Select multiples of 4 from 4 to 40

# Configure la police d'écriture
font = pygame.font.SysFont(None, 30)

# Crée un text object pour chaque taille de plateau de jeu, le nombre de joueurs et le nombre de barrières
board_text_objects = [font.render(size, True, (255, 255, 255)) for size in board_sizes]
players_text_objects = [font.render(player, True, (255, 255, 255)) for player in num_players]
barriers_text_objects = [font.render(str(barrier), True, (255, 255, 255)) for barrier in num_barriers]

# Calcule la position de chaque text sur la fenetre
board_text_positions = [
    (TAILLE_ECRAN[0] // 4 - text.get_width() // 2, TAILLE_ECRAN[1] // 4 - text.get_height() // 2 + 100 * i - 60) for
    i, text in enumerate(board_text_objects)]
players_text_positions = [
    (3 * TAILLE_ECRAN[0] // 4 - text.get_width() // 2, TAILLE_ECRAN[1] // 4 - text.get_height() // 2 + 100 * i - 60) for
    i, text in enumerate(players_text_objects)]
barriers_text_positions = [
    (TAILLE_ECRAN[0] // 2 - text.get_width() // 2, TAILLE_ECRAN[1] // 4 - text.get_height() // 2 + 50 * i - 60) for
    i, text in enumerate(barriers_text_objects)]

# Calcule la position de chaque rectangle sur la fenetre
board_rect_positions = [pygame.Rect(pos[0] - 10, pos[1] - 10, text.get_width() + 20, text.get_height() + 20) for pos, text in
                        zip(board_text_positions, board_text_objects)]
players_rect_positions = [pygame.Rect(pos[0] - 10, pos[1] - 10, text.get_width() + 20, text.get_height() + 20) for pos, text in
                          zip(players_text_positions, players_text_objects)]
barriers_rect_positions = [pygame.Rect(pos[0] - 10, pos[1] - 10, text.get_width() + 20, text.get_height() + 20) for pos, text in
                           zip(barriers_text_positions, barriers_text_objects)]


# Crée un bouton de validation
validation_text = font.render("Valider", True, (255, 255, 255))
validation_position = (TAILLE_ECRAN[0] // 2 - validation_text.get_width() // 2, TAILLE_ECRAN[1] - validation_text.get_height() - 150)
validation_rect = pygame.Rect(validation_position[0] - 10, validation_position[1] - 10, validation_text.get_width() + 20, validation_text.get_height() + 20)


# Variables pour stocker l'index sélectionné de chaque option
selected_board_size_index = None
selected_num_players_index = None
selected_num_barriers_index = None


# Fonction pour vérifier si un rectangle est cliqué
def is_clicked(rect, mouse_pos):
    return rect.collidepoint(mouse_pos)


# Boucle principale du jeu
running = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Vérifie si l'un des rectangles de taille de plateau est cliqué
            for i, rect in enumerate(board_rect_positions):
                if is_clicked(rect, mouse_pos):
                    selected_board_size_index = i

            # Vérifie si l'un des rectangles de nombre de joueurs est cliqué
            for i, rect in enumerate(players_rect_positions):
                if is_clicked(rect, mouse_pos):
                    selected_num_players_index = i

            # Vérifie si l'un des rectangles de nombre de barrières est cliqué
            for i, rect in enumerate(barriers_rect_positions[:len(num_barriers)]):
                if is_clicked(rect, mouse_pos):
                    selected_num_barriers_index = i

            # Vérifie si le bouton de validation est cliqué
            if is_clicked(validation_rect, mouse_pos):
                # Vérifie si toutes les options sont sélectionnées
                if selected_board_size_index is not None and selected_num_players_index is not None and selected_num_barriers_index is not None:
                    # Exécute le script "selection.py" avec les options sélectionnées
                    subprocess.call(["python", "game.py", board_sizes[selected_board_size_index], num_players[selected_num_players_index], str(num_barriers[selected_num_barriers_index])])
                    running = False

    # Dessine la fenetre
    fenetre.fill((0, 0, 0))

    # Dessine les rectangles et les textes de taille de plateau
    for i, rect in enumerate(board_rect_positions):
        if i == selected_board_size_index:
            pygame.draw.rect(fenetre, (255, 0, 0), rect)
            text_rect = board_text_objects[i].get_rect(center=rect.center)
            fenetre.blit(board_text_objects[i], text_rect)
        else:
            pygame.draw.rect(fenetre, (255, 255, 255), rect, 2)
            text_rect = board_text_objects[i].get_rect(center=rect.center)
            fenetre.blit(board_text_objects[i], text_rect)

    # Dessine les rectangles et les textes de nombre de joueurs
    for i, rect in enumerate(players_rect_positions):
        if i == selected_num_players_index:
            pygame.draw.rect(fenetre, (255, 0, 0), rect)
            text_rect = players_text_objects[i].get_rect(center=rect.center)
            fenetre.blit(players_text_objects[i], text_rect)
        else:
            pygame.draw.rect(fenetre, (255, 255, 255), rect, 2)
            text_rect = players_text_objects[i].get_rect(center=rect.center)
            fenetre.blit(players_text_objects[i], text_rect)

    # Dessine les rectangles et les textes de nombre de barrières
    for i, rect in enumerate(barriers_rect_positions[:len(num_barriers)]):
        if i == selected_num_barriers_index:
            pygame.draw.rect(fenetre, (255, 0, 0), rect)
            text_rect = barriers_text_objects[i].get_rect(center=rect.center)
            fenetre.blit(barriers_text_objects[i], text_rect)
        else:
            pygame.draw.rect(fenetre, (255, 255, 255), rect, 2)
            text_rect = barriers_text_objects[i].get_rect(center=rect.center)
            fenetre.blit(barriers_text_objects[i], text_rect)

    # Dessine le bouton de validation
    pygame.draw.rect(fenetre, (0, 255, 0), validation_rect)
    text_rect = validation_text.get_rect(center=validation_rect.center)
    fenetre.blit(validation_text, text_rect)

    # Actualise l'affichage de la fenetre
    pygame.display.flip()

# Quitte pygame
pygame.quit()
sys.exit()
