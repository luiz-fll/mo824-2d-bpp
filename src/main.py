import time
import csv

from carrega_json import carregar_instancia_json
from heuristica_fff import heuristica_fff
from heuristica_hff import heuristica_hff
from grasp import GRASP

# Funções auxiliares para escrever no CSV
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
    
    instance_list = [
        "in/1.json", "in/10.json", "in/20.json", "in/21.json",
        "in/40.json", "in/60.json", "in/70.json", "in/100.json",
        "in/140.json", "in/200.json", "in/250.json", "in/500.json",
        "in/650.json", "in/800.json", "in/900.json"
    ]

    ARQ_HEURISTICAS = "results/resultados_heuristicas.csv"
    ARQ_GRASP = "results/resultados_grasp.csv"

    inicializar_csv(ARQ_HEURISTICAS, ["Instancia", "Metodo", "Bins", "Tempo(s)"])
    inicializar_csv(ARQ_GRASP, ["Instancia", "Construcao", "Busca", "Bins", "Tempo(s)", "Iteracoes_Totais"])

    ITERACOES_MAX = 10000
    TEMPO_MAX = 600 
    ALPHA = 0.2

    print(f"{'='*80}")
    print(f"{'INICIANDO EXPERIMENTOS 2D-BPP COM LOG EM CSV':^80}")
    print(f"{'='*80}\n")

    for instance_name in instance_list:
        print(f"\n{'-'*80}")
        print(f"PROCESSANDO: {instance_name}")
        
        def get_dados(): return carregar_instancia_json(instance_name)
        
        dados_base = get_dados()
        if not dados_base or not dados_base[3]:
            print(f"Erro na instância {instance_name}. Pulando.")
            continue
        l_c, a_c, max_c, itens = dados_base

        print(">>> Executando Heurísticas...")
        
        # FFF
        start = time.time()
        bins_fff = len(heuristica_fff(l_c, a_c, max_c, itens))
        tempo_fff = time.time() - start
        salvar_linha_csv(ARQ_HEURISTICAS, [instance_name, "FFF", bins_fff, f"{tempo_fff:.4f}"])
        print(f"  [FFF] {bins_fff} bins em {tempo_fff:.4f}s")

        # HFF
        start = time.time()
        bins_hff = len(heuristica_hff(l_c, a_c, max_c, itens))
        tempo_hff = time.time() - start
        salvar_linha_csv(ARQ_HEURISTICAS, [instance_name, "HFF", bins_hff, f"{tempo_hff:.4f}"])
        print(f"  [HFF] {bins_hff} bins em {tempo_hff:.4f}s")

        estrategias = [
            ("fff", "first_improving"), ("fff", "best_improving"),
            ("hff", "first_improving"), ("hff", "best_improving")
        ]

        print("\n>>> Executando GRASP...")
        for constr, busca in estrategias:
            nome_grasp = f"GRASP({constr.upper()}+{busca.split('_')[0].title()})"
            print(f"  -> {nome_grasp}...", end="", flush=True)
            
            grasp = GRASP(ITERACOES_MAX, TEMPO_MAX, constr, busca, ALPHA)
            melhor_sol, iteracoes = grasp.executar(instance_name)
            
            tempo_total = time.time() - grasp.tempo_inicio
            num_bins = len(melhor_sol) if melhor_sol else "N/A"
            
            salvar_linha_csv(ARQ_GRASP, [
                instance_name, 
                constr.upper(), 
                busca, 
                num_bins, 
                f"{tempo_total:.2f}", 
                iteracoes
            ])
            print(f" Concluído: {num_bins} bins em {tempo_total:.2f}s ({iteracoes} iterações)")

    print(f"\n{'='*80}")
    print("EXPERIMENTOS FINALIZADOS. RESULTADOS SALVOS EM CSV.")