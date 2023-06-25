import pygame
import sys

# Dimensions de la fenêtre de jeu
WIDTH = 600
HEIGHT = 600

# Dimensions du plateau de jeu
BOARD_SIZE = 9
CELL_SIZE = WIDTH // BOARD_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialise Pygame
pygame.init()

# Crée la fenêtre de jeu
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")

# Classe représentant le jeu Quoridor
class QuoridorGame:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.players = [1, 2]
        self.current_player = 1
        self.winner = None

    def get_valid_moves(self, player):
        # Renvoie les mouvements valides pour un joueur donné
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 0:
                    valid_moves.append((row, col))
        return valid_moves

    def make_move(self, move, player):
        # Effectue un mouvement pour un joueur donné
        row, col = move
        self.board[row][col] = player

    def is_winner(self, player):
        # Vérifie si un joueur a gagné
        target_row = 0 if player == 1 else BOARD_SIZE - 1
        for col in range(BOARD_SIZE):
            if self.board[target_row][col] == player:
                return True
        return False

    def switch_player(self):
        # Change le joueur courant
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def evaluate_board(self):
        # Évalue la situation actuelle du plateau de jeu
        if self.is_winner(1):
            return -1
        elif self.is_winner(2):
            return 1
        else:
            return 0

    def minimax(self, depth, maximizing_player):
        # Implémentation de l'algorithme Minimax avec élagage Alpha-Beta
        if depth == 0 or self.is_game_over():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float("-inf")
            valid_moves = self.get_valid_moves(self.players[1])
            for move in valid_moves:
                self.make_move(move, self.players[1])
                eval = self.minimax(depth - 1, False)
                self.make_move(move, 0)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            valid_moves = self.get_valid_moves(self.players[0])
            for move in valid_moves:
                self.make_move(move, self.players[0])
                eval = self.minimax(depth - 1, True)
                self.make_move(move, 0)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self):
        # Récupère le meilleur mouvement pour l'IA en utilisant l'algorithme Minimax
        valid_moves = self.get_valid_moves(self.players[1])
        best_eval = float("-inf")
        best_move = None
        for move in valid_moves:
            self.make_move(move, self.players[1])
            eval = self.minimax(3, False)  # Profondeur de recherche de l'IA
            self.make_move(move, 0)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def is_game_over(self):
        # Vérifie si le jeu est terminé
        return self.is_winner(1) or self.is_winner(2)

    def handle_event(self, event):
        # Gère les événements de la souris
        if event.type == pygame.MOUSEBUTTONDOWN and not self.is_game_over() and self.current_player == 1:
            mouse_pos = pygame.mouse.get_pos()
            col = mouse_pos[0] // CELL_SIZE
            row = mouse_pos[1] // CELL_SIZE
            move = (row, col)
            if move in self.get_valid_moves(1):
                self.make_move(move, 1)
                if self.is_winner(1):
                    self.winner = 1
                else:
                    self.current_player = 2
                    # Laisse l'IA jouer
                    ai_move = self.get_best_move()
                    if ai_move is not None:
                        self.make_move(ai_move, 2)
                        if self.is_winner(2):
                            self.winner = 2

    def draw(self):
        # Dessine le plateau de jeu
        window.fill(WHITE)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.board[row][col] == 1:
                    pygame.draw.rect(window, BLACK, rect)
                elif self.board[row][col] == 2:
                    pygame.draw.rect(window, RED, rect)
        pygame.display.update()  # Ajout de cette ligne pour mettre à jour l'affichage


# Crée une instance du jeu Quoridor
game = QuoridorGame()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_event(event)
    game.draw()
    if game.winner is not None:
        print("Le joueur", game.winner, "a gagné !")
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()
