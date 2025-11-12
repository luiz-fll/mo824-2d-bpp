import math
import csv
import sys
from carrega_json import carregar_instancia_json

def calcular_lower_bound(l_container, a_container, itens):
    """
    Calcula o limite inferior teórico (Lower Bound L1) baseada na área.
    """
    area_bin = l_container * a_container
    
    if area_bin == 0:
        return float('inf') 
        
    area_total_itens = sum(item.largura * item.altura for item in itens)
    
    return math.ceil(area_total_itens / area_bin)

def inicializar_csv(nome_arquivo, cabecalho):
    """Cria o arquivo CSV e escreve o cabeçalho."""
    try:
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cabecalho)
    except IOError as e:
        print(f"Erro ao inicializar CSV {nome_arquivo}: {e}")
        sys.exit(1)

def salvar_linha_csv(nome_arquivo, dados):
    """Adiciona uma linha de resultados ao arquivo CSV."""
    try:
        with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(dados)
    except IOError as e:
        print(f"Erro ao salvar linha no CSV {nome_arquivo}: {e}")

if __name__ == "__main__":
    
    instance_list = [
        "in/1.json", "in/3.json", "in/4.json", "in/5.json", "in/6.json", "in/7.json", "in/10.json", "in/20.json", "in/21.json", "in/40.json", "in/60.json", "in/70.json", 
        "in/100.json", "in/140.json", "in/200.json", "in/250.json", "in/490.json", "in/491.json", "in/492.json", "in/493.json", "in/494.json", "in/495.json", "in/496.json", 
        "in/497.json", "in/498.json", "in/499.json", "in/500.json", "in/650.json", "in/700.json", "in/701.json", "in/702.json", "in/703.json", "in/704.json", "in/705.json", 
        "in/706.json", "in/707.json", "in/708.json", "in/709.json", "in/800.json", "in/890.json", "in/891.json", "in/892.json", "in/893.json", "in/894.json", "in/895.json", 
        "in/896.json", "in/897.json", "in/898.json", "in/899.json", "in/900.json"
    ]
    
    ARQUIVO_CSV_SAIDA = "results/resultados_lower_bound.csv"
    CABECALHO = ["Instancia", "Lower_Bound_Area(L1)"]

    inicializar_csv(ARQUIVO_CSV_SAIDA, CABECALHO)

    for nome_arquivo in instance_list:
        dados = carregar_instancia_json(nome_arquivo)
        
        if dados:
            l_cont, a_cont, max_cont, itens = dados
            lb = calcular_lower_bound(l_cont, a_cont, itens)
            
            salvar_linha_csv(ARQUIVO_CSV_SAIDA, [nome_arquivo, lb])
        else:
            print(f"  -> ERRO ao carregar {nome_arquivo}.")
            salvar_linha_csv(ARQUIVO_CSV_SAIDA, [nome_arquivo, "Erro_Carregamento"])