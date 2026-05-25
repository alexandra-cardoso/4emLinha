import math
from Player import Player

class MinimaxAIPlayer(Player):

    def __init__(self, piece, max_depth=5):
        super().__init__(piece)          # inicializa self.piece na classe base
        self.max_depth = max_depth       # profundidade máxima de pesquisa
        self.opponent_piece = 2 if piece == 1 else 1

    def get_move(self, board):
        # Inicia o minimax como jogador maximizante e devolve só a coluna
        _, col = self._minimax(board, self.max_depth, -math.inf, math.inf, True)
        return col

    def _minimax(self, board, depth, alpha, beta, maximizing):
        valid_moves = board.get_valid_moves()

        # Casos terminais: vitória, derrota, empate ou profundidade máxima atingida
        if board.check_winner(self.piece):
            return (1_000_000 + depth, None)   # vitória — bónus por ganhar mais cedo
        if board.check_winner(self.opponent_piece):
            return (-1_000_000 - depth, None)  # derrota — penalização por perder mais tarde
        if board.is_board_full():
            return (0, None)                   # empate
        if depth == 0:
            return (self.evaluate_board(board, self.piece), None)  # avaliação heurística

        best_col = valid_moves[len(valid_moves) // 2]  # fallback: coluna central

        if maximizing:
            # Turno do agente: maximizar a pontuação
            best_score = -math.inf
            for col in self._order_moves(valid_moves, board):
                new_board = board.copy()
                new_board.drop_piece(col, self.piece)
                score, _ = self._minimax(new_board, depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score = score
                    best_col = col
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break  # corte beta: o adversário nunca escolheria este ramo
            return (best_score, best_col)
        else:
            # Turno do adversário: minimizar a pontuação
            best_score = math.inf
            for col in self._order_moves(valid_moves, board):
                new_board = board.copy()
                new_board.drop_piece(col, self.opponent_piece)
                score, _ = self._minimax(new_board, depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    best_col = col
                beta = min(beta, best_score)
                if alpha >= beta:
                    break  # corte alfa: o agente nunca escolheria este ramo
            return (best_score, best_col)

    def _order_moves(self, valid_moves, board):
        # Ordena jogadas do centro para as bordas — melhora a eficiência da poda alpha-beta
        cols = board.grid.shape[1]
        center = cols // 2
        return sorted(valid_moves, key=lambda c: abs(c - center))

    def evaluate_board(self, board, player):
        # Avalia o tabuleiro atribuindo pontuação positiva ao agente e negativa ao adversário
        grid = board.grid
        rows, cols = grid.shape
        n = board.n_connect  # tamanho da sequência necessária para ganhar
        opponent = self.opponent_piece
        score = 0

        # Peças no centro valem mais — controlam mais diagonais e colunas
        center_col = cols // 2
        center_array = [grid[r][center_col] for r in range(rows)]
        score += center_array.count(player) * 6

        # Avaliar todas as janelas de tamanho n em cada direção
        for r in range(rows):                        # horizontal
            for c in range(cols - n + 1):
                window = [grid[r][c + i] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        for c in range(cols):                        # vertical
            for r in range(rows - n + 1):
                window = [grid[r + i][c] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        for r in range(rows - n + 1):               # diagonal \
            for c in range(cols - n + 1):
                window = [grid[r + i][c + i] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        for r in range(rows - n + 1):               # diagonal /
            for c in range(n - 1, cols):
                window = [grid[r + i][c - i] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        return score

    def _score_window(self, window, player, opponent, n):
        # Pontua uma janela de n células: bónus por sequências do agente, penalização por ameaças do adversário
        score = 0
        player_count   = window.count(player)
        opponent_count = window.count(opponent)
        empty_count    = window.count(0)

        if player_count == n:                              # sequência completa (já capturada no check_winner)
            score += 500
        elif player_count == n - 1 and empty_count == 1:  # a uma peça de ganhar
            score += 50
        elif player_count == n - 2 and empty_count == 2:  # duas peças seguidas com espaço
            score += 10

        if opponent_count == n - 1 and empty_count == 1:  # adversário a uma peça de ganhar — bloquear!
            score -= 80
        elif opponent_count == n - 2 and empty_count == 2:
            score -= 5

        return score