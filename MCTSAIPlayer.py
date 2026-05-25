import math
import random
import numpy as np
from Player import Player

class MCTSNode: #temos de criar esta classe de nós para  guardar a árvore
    def __init__(self, board, parent = None, move = None, current_piece = None):
        self.board = board #o estado do tabuleiro neste nó
        self.parent = parent #nó pai: para a Retropropagação
        self.move = move #jogada que nos trouxe a este estado
        self.current_piece = current_piece #guarda a peça que efetuou a jogada

        self.children = [] #nós filhos: proxs jogadas
        self.wins = 0 #quantas vitórias
        self.visits = 0 #quantas vezes explorámos o nó

        self.untried_moves = board.get_valid_moves() # jogadas a partir deste estado ainda não expandidas
    
    def uct_score(self, c_param = 1.41): #calcular a formula UCB1
        if self.visits == 0:
            return float('inf') #damos prioridade a caminhos não explorados
        
        #fórmula:
        exploitation = self.wins / self.visits
        exploration = c_param * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration




class MCTSAIPlayer (Player):
    def __init__(self, piece, max_iterations=1000):
        super().__init__(piece)
        self.max_iterations = max_iterations #nº variavel de iterações
        self.opponent_piece = 2 if piece == 1 else 1
    

    def get_move(self, board):
        p1_count = np.count_nonzero(board.grid == 1)
        p2_count = np.count_nonzero(board.grid == 2)
        root_piece = 2 if p1_count == p2_count else 1

        root = MCTSNode(board, current_piece=root_piece) #raiz da árvore é o estado atual do jogo, e a peça é a que jogou
        
        for _ in range(self.max_iterations):
            node = root

            #fase de seleção:
            while not node.untried_moves and node.children: #enquanto o nó já foi expandido totalmente e o jogo n acabou
                node = max(node.children, key = lambda c: c.uct_score()) #escolhe o filho com maior uct_score

            #fase de expansão:
            if node.untried_moves:
                move = random.choice(node.untried_moves) #vamos escolher uma jogada aleatória dos movimentos ainda por testar
                node.untried_moves.remove(move) # e vamos removê-la das não testadas

                #a peça que vai jogar agora é a adversária da ultima que jogou neste nó
                next_piece = 2 if node.current_piece == 1 else 1

                new_board = node.board.copy() #cria um novo tabuleiro
                new_board.drop_piece(move, next_piece) #faz a jogada

                new_node = MCTSNode(new_board, parent = node, move = move, current_piece=next_piece) #criamos o novo filho, resultante desta jogada
                node.children.append(new_node)
                node = new_node

            #fase 3: simulação 
            resultado = self.simulate(node.board, node.current_piece) #jogar à sorte a partir do nó onde parámos, até o jogo acabar

            #fase backpropagation
            while node is not None:
                node.visits += 1
                if resultado != 0 and resultado == node.current_piece:
                    node.wins += 1
                    
                node = node.parent
            
        #no fim das iterações
        if not root.children:
            valid_moves = board.get_valid_moves()
            return random.choice(valid_moves) if valid_moves else None
        
        best_child = max(root.children, key = lambda c: c.visits)
        return best_child.move
        

    def simulate(self, board, last_piece):
        tabuleiro = board.copy()
        
        if tabuleiro.check_winner(1): #podemos ser nós os vencedores
            return 1
        if tabuleiro.check_winner(2): #ou pode ser o nosso oponente
            return 2
        if tabuleiro.is_board_full(): #se estiver tudo cheio, houve um empate
            return 0
        
        current_piece = 2 if last_piece == 1 else 1
        
        while not tabuleiro.is_board_full():
            moves = tabuleiro.get_valid_moves()
            if not moves: break
            move = random.choice(moves)

            tabuleiro.drop_piece(move, current_piece)
            if tabuleiro.check_winner(current_piece):
                return current_piece
            
            current_piece = 2 if current_piece == 1 else 1
            
        return 0
