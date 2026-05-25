import time
from Connect4Game import Connect4Game
from RandomPlayer import RandomAIPlayer

# Tenta importar os teus agentes (vai dar erro se os ficheiros/classes não existirem com os nomes certos)
try:
    from MinimaxAIPlayer import MinimaxAIPlayer
    from MCTSAIPlayer import MCTSAIPlayer
except ImportError as e:
    print(f"ERRO: Não foi possível importar os teus agentes. Verifica os nomes dos ficheiros e classes! Detalhe: {e}")
    exit()

def correr_bateria_testes(nome_teste, p1, p2, num_jogos=10):
    print(f"\n{'='*50}")
    print(f"A iniciar teste: {nome_teste} ({num_jogos} jogos)")
    print(f"{'='*50}")
    
    game = Connect4Game()
    
    vitorias_p1 = 0
    vitorias_p2 = 0
    empates = 0
    
    tempos_jogos = []
    
    for i in range(num_jogos):
        inicio_jogo = time.time()
        
        # Executa o jogo em modo headless (sem interface gráfica para ser instantâneo)
        vencedor = game.run_game(p1, p2, headless=True)
        
        fim_jogo = time.time()
        duracao = fim_jogo - inicio_jogo
        tempos_jogos.append(duracao)
        
        if vencedor == p1.piece:
            vitorias_p1 += 1
        elif vencedor == p2.piece:
            vitorias_p2 += 1
        else:
            empates += 1
            
        print(f"Jogo {i+1}/{num_jogos} concluído. Vencedor: {vencedor} (Duração: {duracao:.2f}s)")

    # Cálculos para o Excel
    taxa_vitorias_p1 = (vitorias_p1 / num_jogos) * 100
    taxa_vitorias_p2 = (vitorias_p2 / num_jogos) * 100
    duracao_media = sum(tempos_jogos) / num_jogos
    duracao_max = max(tempos_jogos)
    duracao_min = min(tempos_jogos)

    print(f"\n--- RESULTADOS PARA O EXCEL: {nome_teste} ---")
    print(f"Vitórias Jogador 1 (Peça {p1.piece}): {vitorias_p1} ({taxa_vitorias_p1:.1f}%)")
    print(f"Vitórias Jogador 2 (Peça {p2.piece}): {vitorias_p2} ({taxa_vitorias_p2:.1f}%)")
    print(f"Empates: {empates}")
    print(f"Duração Média: {duracao_media:.3f} segundos")
    print(f"Duração Máxima: {duracao_max:.3f} segundos")
    print(f"Duração Mínima: {duracao_min:.3f} segundos")
    print("-" * 50)

if __name__ == "__main__":
    # Define o número de jogos para cada comparação (o enunciado não diz quantos, mas 10 a 20 é um bom número)
    NUM_JOGOS = 10 
    
    # 1. Minimax vs Aleatório
    p_minimax_teste1 = MinimaxAIPlayer(piece=1, max_depth=3)
    p_random_teste1 = RandomAIPlayer(piece=2)
    correr_bateria_testes("Minimax (Depth=3) vs Aleatório", p_minimax_teste1, p_random_teste1, NUM_JOGOS)

    # 2. MCTS vs Aleatório
    p_mcts_teste2 = MCTSAIPlayer(piece=1, max_iterations=500)
    p_random_teste2 = RandomAIPlayer(piece=2)
    correr_bateria_testes("MCTS (Iter=500) vs Aleatório", p_mcts_teste2, p_random_teste2, NUM_JOGOS)

    # O enunciado pede para testar 3 combinações de Minimax vs MCTS
    # Combinação 1 (Ajusta os valores para que o tempo seja idêntico)
    comb1_p1 = MinimaxAIPlayer(piece=1, max_depth=3)
    comb1_p2 = MCTSAIPlayer(piece=2, max_iterations=500)
    correr_bateria_testes("COMB 1: Minimax(d=3) vs MCTS(i=500)", comb1_p1, comb1_p2, NUM_JOGOS)

    # Combinação 2 (Ajusta os valores)
    comb2_p1 = MinimaxAIPlayer(piece=1, max_depth=4)
    comb2_p2 = MCTSAIPlayer(piece=2, max_iterations=2000)
    correr_bateria_testes("COMB 2: Minimax(d=4) vs MCTS(i=2000)", comb2_p1, comb2_p2, NUM_JOGOS)

    # Combinação 3 (Ajusta os valores)
    comb3_p1 = MinimaxAIPlayer(piece=1, max_depth=5)
    comb3_p2 = MCTSAIPlayer(piece=2, max_iterations=5000)
    correr_bateria_testes("COMB 3: Minimax(d=5) vs MCTS(i=5000)", comb3_p1, comb3_p2, NUM_JOGOS)