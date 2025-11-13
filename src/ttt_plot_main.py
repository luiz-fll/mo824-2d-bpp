import time
import csv

from carrega_json import carregar_instancia_json
from grasp import GRASP

def inicializar_csv(nome_arquivo, cabecalho):
    """Cria o arquivo CSV e escreve o cabeçalho se ele não existir."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)

def salvar_linha_csv(nome_arquivo, dados):
    """Adiciona uma linha de resultados ao arquivo CSV."""
    with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(dados)

if __name__ == "__main__":
    
    instance_list_target = [
        ["in/20.json", 11], 
        ["in/490.json", 15], 
        ["in/890.json", 105], 
    ]

    seed_list = [
        619421, 231586, 610516, 82352, 42, 363670, 764828, 364535, 432140, 679928
    ]

    ARQ_GRASP = "results/resultados_ttt_plot.csv"

    inicializar_csv(ARQ_GRASP, ["Instancia", "Construcao", "Busca", "SEED", "Bins", "Iteracoes_Totais", "Valor Alvo", "Atingiu valor alvo?", "Tempo até valor alvo"])

    ITERACOES_MAX = 100000000
    TEMPO_MAX = 900 
    ALPHA = 0.2

    for instance in instance_list_target:
        instance_name = instance[0]
        print(f"PROCESSANDO: {instance_name}")
        instance_target = instance[1]

        dados_base = carregar_instancia_json(instance_name)

        for seed in seed_list:
            print(f"SEED: {seed}")
            l_c, a_c, max_c, itens = dados_base

            estrategias = [
                ("fff", "first_improving"), ("fff", "best_improving"),
                ("hff", "first_improving"), ("hff", "best_improving")
            ]

            for constr, busca in estrategias:
                nome_grasp = f"GRASP({constr.upper()}+{busca.split('_')[0].title()})"
                
                grasp = GRASP(ITERACOES_MAX, TEMPO_MAX, constr, busca, ALPHA, seed)
                melhor_sol, iteracoes, valor_alvo, atingiu_valor_alvo, tempo_ate_alvo = grasp.executar(instance_name, instance_target)
                
                tempo_total = time.time() - grasp.tempo_inicio
                num_bins = len(melhor_sol) if melhor_sol else "N/A"
                
                salvar_linha_csv(ARQ_GRASP, [
                    instance_name, 
                    constr.upper(), 
                    busca, 
                    seed,
                    num_bins, 
                    iteracoes,
                    valor_alvo,
                    atingiu_valor_alvo,
                    tempo_ate_alvo
                ])

    print("EXPERIMENTOS FINALIZADOS. RESULTADOS SALVOS EM CSV.")