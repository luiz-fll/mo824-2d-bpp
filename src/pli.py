import gurobipy as gp
from gurobipy import GRB
import time
import csv

from carrega_json import carregar_instancia_json


def inicializar_csv(nome_arquivo, cabecalho):
    """Cria o arquivo CSV e escreve o cabeçalho."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        writer.writeheader()

def salvar_linha_csv(nome_arquivo, dados_dict, cabecalho):
    """Adiciona uma linha de resultados ao arquivo CSV."""
    with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        writer.writerow(dados_dict)


def resolver_pli(instance_name, time_limit=600):
    """
    Resolve a instância 2D-BPP, imprime o log e retorna um dicionário de resultados.
    """
    
    result = {
        "Instancia": instance_name,
        "Status": "Erro_Carregamento",
        "Bins_Usados": "N/A",
        "Lower_Bound": "N/A",
        "Tempo(s)": 0.0
    }
    
    try:
        l_container, a_container, _, itens = carregar_instancia_json(instance_name)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{instance_name}' não encontrado.")
        result["Status"] = "Erro_Arquivo_Nao_Encontrado"
        return result
    except Exception as e:
        print(f"Erro ao carregar instância: {e}")
        return result

    n = len(itens)
    m_bins = n 
    I = range(n) 
    J = range(m_bins)
    P = [(i, k) for i in I for k in I if i < k]
    w = [item.largura for item in itens]
    h = [item.altura for item in itens]
    W = l_container
    H = a_container
    M = max(W, H)
    
    print(f"\nIniciando Gurobi para instância: {instance_name}")
    print(f"Itens: {n}, Bins disponíveis (m): {m_bins}, Dimensões: {W}x{H}")
    
    try:
        m = gp.Model("2D_BPP_PLI")
        
        # Variáveis
        y = m.addVars(J, vtype=GRB.BINARY, name="y")
        x = m.addVars(I, J, vtype=GRB.BINARY, name="x")
        px = m.addVars(I, J, vtype=GRB.CONTINUOUS, lb=0, name="px")
        py = m.addVars(I, J, vtype=GRB.CONTINUOUS, lb=0, name="py")
        a_ik = m.addVars(P, J, vtype=GRB.BINARY, name="i_left_k")
        a_ki = m.addVars(P, J, vtype=GRB.BINARY, name="k_left_i")
        b_ik = m.addVars(P, J, vtype=GRB.BINARY, name="i_below_k")
        b_ki = m.addVars(P, J, vtype=GRB.BINARY, name="k_below_i")

        # Restrições
        m.addConstrs((x.sum(i, '*') == 1 for i in I), name="alocacao_unica")
        m.addConstrs((px[i, j] + w[i] <= W + M * (1 - x[i, j]) for i in I for j in J), name="limite_X")
        m.addConstrs((py[i, j] + h[i] <= H + M * (1 - x[i, j]) for i in I for j in J), name="limite_Y")
        for i, k in P:
            for j in J:
                m.addConstr(px[i, j] + w[i] <= px[k, j] + M * (1 - a_ik[i, k, j]), name=f"i{i}_left_k{k}_j{j}")
                m.addConstr(px[k, j] + w[k] <= px[i, j] + M * (1 - a_ki[i, k, j]), name=f"k{k}_left_i{i}_j{j}")
                m.addConstr(py[i, j] + h[i] <= py[k, j] + M * (1 - b_ik[i, k, j]), name=f"i{i}_below_k{k}_j{j}")
                m.addConstr(py[k, j] + h[k] <= py[i, j] + M * (1 - b_ki[i, k, j]), name=f"k{k}_below_i{i}_j{j}")
        m.addConstrs((a_ik[i, k, j] + a_ki[i, k, j] + b_ik[i, k, j] + b_ki[i, k, j] >= x[i, j] + x[k, j] - 1 
                      for i, k in P for j in J), name="logica_OR")
        m.addConstrs((x[i, j] <= y[j] for i in I for j in J), name="link_x_y")

        # Objetivo
        m.setObjective(y.sum(), GRB.MINIMIZE)
        m.setParam('TimeLimit', time_limit)
        
        # Otimiza
        start_time = time.time()
        m.optimize()
        end_time = time.time()
        
        result["Tempo(s)"] = f"{end_time - start_time:.2f}" # Usamos tempo real

        # Coleta de resultados
        if m.Status == GRB.OPTIMAL:
            result["Status"] = "Otimo"
            result["Bins_Usados"] = int(m.ObjVal)
            result["Lower_Bound"] = int(m.ObjBound)
        elif m.Status == GRB.TIME_LIMIT:
            result["Status"] = "Limite_Tempo"
            if m.SolCount > 0:
                result["Bins_Usados"] = int(m.ObjVal)
                result["Lower_Bound"] = int(m.ObjBound)
            else:
                result["Status"] = "Limite_Tempo_Sem_Sol"
        elif m.Status == GRB.INFEASIBLE:
            result["Status"] = "Inviavel"
        elif m.Status == GRB.UNBOUNDED:
            result["Status"] = "Ilimitado"
        else:
             result["Status"] = f"Gurobi_Status_{m.Status}"

        # Impressão no console (mantida)
        print(f"\n--- Solução Encontrada (Status: {result['Status']}) ---")
        print(f"Tempo de execução: {result['Tempo(s)']}s")
        if m.SolCount > 0:
            print(f"Total de containers (ObjVal): {result['Bins_Usados']}")
            print(f"Lower Bound (ObjBound): {result['Lower_Bound']}")

    except gp.GurobiError as e:
        print(f"Erro do Gurobi: {e.errno}: {e}")
        result["Status"] = f"Erro_Gurobi_{e.errno}"
    except Exception as e:
        print(f"Erro: {e}")
        result["Status"] = f"Erro_Python"
        
    return result

if __name__ == "__main__":
    
    # Lista de instâncias a serem executadas
    instance_list = [
        "in/1.json", "in/3.json", "in/4.json", "in/5.json", "in/6.json", "in/7.json", "in/10.json", "in/20.json", "in/21.json", "in/40.json", "in/60.json", "in/70.json", 
        "in/100.json", "in/140.json", "in/200.json", "in/250.json", "in/490.json", "in/491.json", "in/492.json", "in/493.json", "in/494.json", "in/495.json", "in/496.json", 
        "in/497.json", "in/498.json", "in/499.json", "in/500.json", "in/650.json", "in/700.json", "in/701.json", "in/702.json", "in/703.json", "in/704.json", "in/705.json", 
        "in/706.json", "in/707.json", "in/708.json", "in/709.json", "in/800.json", "in/890.json", "in/891.json", "in/892.json", "in/893.json", "in/894.json", "in/895.json", 
        "in/896.json", "in/897.json", "in/898.json", "in/899.json", "in/900.json"
    ]
    
    ARQUIVO_CSV_PLI = "results/resultados_pli.csv"
    CABECALHO_CSV = ["Instancia", "Status", "Bins_Usados", "Lower_Bound", "Tempo(s)"]
    
    LIMITE_TEMPO = 600 

    inicializar_csv(ARQUIVO_CSV_PLI, CABECALHO_CSV)
    for instancia in instance_list:
        resultado = resolver_pli(instancia, time_limit=LIMITE_TEMPO)
        
        # Salva a linha no CSV
        salvar_linha_csv(ARQUIVO_CSV_PLI, resultado, CABECALHO_CSV)
        
        print(f"Instância {instancia} concluída.")
        print("-" * 40)

    print(f"Processamento de todas as instâncias concluído.")