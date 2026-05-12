from Player import Player
import random

class MCTSAIPlayer (Player):
    def __init__(self, piece, iters=1000):
        super().__init__(piece)
        self.iters = iters #nº variavel de iterações
    
    
    def get_move(self, board):
        moves = board.get_valid_moves()
        
        if len(moves) == 1:
            return moves[0]
        
        move_valor = {move: 0 for move in moves}
        for _ in range(self.iters):
            move = random.choice(moves)
            tempBoard = board.copy()
            tempBoard.drop_piece(move, self.piece)
            resultado = self.simulate(tempBoard)
            
            if resultado == self.piece:
                move_valor[move] += 1
        
        return max(move_valor, key = move_valor.get)
    
    def simulate(self, board):
        tabuleiro = board.copy()
        opponent = 2 if self.piece == 1 else 1
        
        if board.is_board_full():
            print("Empate")
        elif board.check_winner(self.piece):
            print("És o vencedor")
        elif board.check_winner(opponent):
            print("Perdeste")

        #resto da logica jogo
        
        pass
    
    