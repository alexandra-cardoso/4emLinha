import math
from Player import Player

class MinimaxAIPlayer(Player):
  

    def __init__(self, piece, max_depth=5):
       
        super().__init__(piece)     
        self.max_depth = max_depth
        self.opponent_piece = 2 if piece == 1 else 1

    def get_move(self, board):
        _, col = self._minimax(board, self.max_depth, -math.inf, math.inf, True)
        return col


    def _minimax(self, board, depth, alpha, beta, maximizing):
       
        valid_moves = board.get_valid_moves()

    
        if board.check_winner(self.piece):
            return (1_000_000 + depth, None)   # vitória (mais cedo = melhor)
        if board.check_winner(self.opponent_piece):
            return (-1_000_000 - depth, None)  # derrota (mais tarde = menos pior)
        if board.is_board_full():
            return (0, None)                   # empate
        if depth == 0:
            return (self.evaluate_board(board, self.piece), None)

        best_col = valid_moves[len(valid_moves) // 2]  # coluna central como fallback

        if maximizing:
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
                    break  # corte beta
            return (best_score, best_col)
        else:
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
                    break  # corte alfa
            return (best_score, best_col)

    def _order_moves(self, valid_moves, board):
        cols = board.grid.shape[1]
        center = cols // 2
        return sorted(valid_moves, key=lambda c: abs(c - center))

    
    def evaluate_board(self, board, player):
        grid = board.grid
        rows, cols = grid.shape
        n = board.n_connect                             
        opponent = self.opponent_piece
        score = 0

       
        center_col = cols // 2
        center_array = [grid[r][center_col] for r in range(rows)]
        score += center_array.count(player) * 6

        
        for r in range(rows):
            for c in range(cols - 3):
                window = [grid[r][c + i] for i in range(4)]
                score += self._score_window(window, player, opponent)

        
        for c in range(cols):
            for r in range(rows - 3):
                window = [grid[r + i][c] for i in range(4)]
                score += self._score_window(window, player, opponent)

       
        for r in range(rows - 3):
            for c in range(cols - 3):
                window = [grid[r + i][c + i] for i in range(4)]
                score += self._score_window(window, player, opponent)

        
        for r in range(rows - 3):
            for c in range(3, cols):
                window = [grid[r + i][c - i] for i in range(4)]
                score += self._score_window(window, player, opponent)

        return score

    def _score_window(self, window, player, opponent, n):          # FIX 2: n dinâmico
        score = 0
        player_count   = window.count(player)
        opponent_count = window.count(opponent)
        empty_count    = window.count(0)
 
        if player_count == n:
            score += 500
        elif player_count == n - 1 and empty_count == 1:
            score += 50
        elif player_count == n - 2 and empty_count == 2:
            score += 10
 
        if opponent_count == n - 1 and empty_count == 1:
            score -= 80           # bloquear ameaça imediata do adversário
        elif opponent_count == n - 2 and empty_count == 2:
            score -= 5
 
        return score