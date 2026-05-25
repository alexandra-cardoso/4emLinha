import math
from Player import Player

class MinimaxAIPlayer(Player):

    def __init__(self, piece, max_depth=5):
        # Inicializa a classe base com a nossa peça (1 ou 2)
        super().__init__(piece)          
        # Quantas jogadas à frente o algoritmo consegue "ver"
        self.max_depth = max_depth       

    def get_move(self, board):
        # Arranca o algoritmo Minimax e guarda apenas a coluna escolhida
        _, col = self._minimax(board, self.max_depth, -math.inf, math.inf, True)
        return col

    def _minimax(self, board, depth, alpha, beta, maximizing):
        valid_moves = board.get_valid_moves()
        # Descobre quem é o adversário de forma dinâmica
        opponent_piece = 2 if self.piece == 1 else 1

        # Vitória, Derrota, Empate ou Limite de Profundidade)
        if board.check_winner(self.piece):
            return (1_000_000 + depth, None)   # Ganhámos! Bónus por ser rápido
        if board.check_winner(opponent_piece):
            return (-1_000_000 - depth, None)  # Perdemos! Penalização por perder tarde
        if board.is_board_full():
            return (0, None)                   # Empate (neutro)
        if depth == 0:
            return (self.evaluate_board(board, self.piece), None)  # Chegámos ao limite, avalia o tabuleiro

        # Jogada de segurança (meio do tabuleiro) caso algo falhe
        best_col = valid_moves[len(valid_moves) // 2]  

        #Tentar ter a maior pontuação possível
        if maximizing:
            best_score = -math.inf
            for col in self._order_moves(valid_moves, board):
                new_board = board.copy() # Simula num tabuleiro falso
                new_board.drop_piece(col, self.piece)
                
                # Chama o minimax para o turno do adversário
                score, _ = self._minimax(new_board, depth - 1, alpha, beta, False)
                
                if score > best_score:
                    best_score = score
                    best_col = col
                
                # Poda Alpha-Beta (se já temos uma jogada ótima, não perdemos tempo a ver o resto)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break  
            return (best_score, best_col)
            
        #Ele vai tentar dar-nos a menor pontuação possível
        else:
            best_score = math.inf
            for col in self._order_moves(valid_moves, board):
                new_board = board.copy()
                new_board.drop_piece(col, opponent_piece)
                
                score, _ = self._minimax(new_board, depth - 1, alpha, beta, True)
                
                if score < best_score:
                    best_score = score
                    best_col = col
                    
                beta = min(beta, best_score)
                if alpha >= beta:
                    break  
            return (best_score, best_col)

    def _order_moves(self, valid_moves, board):
        # testar primeiro as colunas do meio.
        # Assim a poda Alpha-Beta corta muito mais ramos inúteis.
        grid = board.grid
        cols = len(grid[0]) if len(grid) > 0 else 7
        center = cols // 2
        return sorted(valid_moves, key=lambda c: abs(c - center))

    def evaluate_board(self, board, player):
        # Esta função dá uma "nota" ao tabuleiro atual
        grid = board.grid
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 7
        
        # Tenta ir buscar o limite para ganhar, previne erros caso os testes sejam diferentes
        try:
            n = board.n_connect
        except AttributeError:
            n = 4

        opponent = 2 if player == 1 else 1
        score = 0
        
        # Ter peças no centro vale ouro, ganha pontos extra!
        center_col = cols // 2
        center_array = [grid[r][center_col] for r in range(rows)]
        score += center_array.count(player) * 6

        # Avaliar todas as linhas possíveis (Horizontal, Vertical, Diagonal)
        for r in range(rows):                        
            for c in range(cols - n + 1):
                window = [grid[r][c + i] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        for c in range(cols):                        
            for r in range(rows - n + 1):
                window = [grid[r + i][c] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        for r in range(rows - n + 1):               
            for c in range(cols - n + 1):
                window = [grid[r + i][c + i] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        for r in range(rows - n + 1):               
            for c in range(n - 1, cols):
                window = [grid[r + i][c - i] for i in range(n)]
                score += self._score_window(window, player, opponent, n)

        return score

    def _score_window(self, window, player, opponent, n):
        # Dá pontos se estivermos quase a ganhar e tira pontos se for o adversário
        score = 0
        player_count   = window.count(player)
        opponent_count = window.count(opponent)
        empty_count    = window.count(0)

        # Ofensiva: valorizar as nossas sequências
        if player_count == n:                              
            score += 500
        elif player_count == n - 1 and empty_count == 1:  
            score += 50
        elif player_count == n - 2 and empty_count == 2:  
            score += 10

        # bloqueia o adversário se ele estiver a uma ou duas peças de ganhar
        if opponent_count == n - 1 and empty_count == 1:  
            score -= 80
        elif opponent_count == n - 2 and empty_count == 2:
            score -= 5

        return score