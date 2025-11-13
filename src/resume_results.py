import csv
import os

def consolidar_resultados(arq_lb, arq_heur, arq_pli, arq_saida):
    """
    Combina os resultados dos três CSVs de entrada em um único CSV de saída.

    Args:
        arq_lb (str): Caminho para o CSV de Lower Bound (L1).
        arq_heur (str): Caminho para o CSV das heurísticas (FFF, HFF).
        arq_pli (str): Caminho para o CSV dos resultados do PLI (Gurobi).
        arq_saida (str): Caminho para o arquivo CSV consolidado de saída.
    """
    
    resultados = {}

    try:
        with open(arq_lb, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                instancia = row['Instancia']
                resultados[instancia] = {}
                resultados[instancia]['Limite teórico'] = row['Lower_Bound_Area(L1)']
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{arq_lb}' não encontrado. Coluna 'Limite teórico' ficará vazia.")

    try:
        with open(arq_heur, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                instancia = row['Instancia']
                metodo = row['Metodo']
                bins = row['Bins']
                
                resultados.setdefault(instancia, {})
                
                if metodo == 'FFF':
                    resultados[instancia]['FFF'] = bins
                elif metodo == 'HFF':
                    resultados[instancia]['HFF'] = bins
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{arq_heur}' não encontrado. Colunas 'FFF' e 'HFF' ficarão vazias.")

    try:
        with open(arq_pli, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                instancia = row['Instancia']
                
                resultados.setdefault(instancia, {})
                
                resultados[instancia]['PLI'] = row['Bins_Usados']
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{arq_pli}' não encontrado. Colunas 'PLI' e 'Bins' ficarão vazias.")

    colunas_saida = ['Instância', 'FFF', 'HFF', 'PLI', 'Limite teórico']

    def extrair_numero_instancia(item_dicionario):
        instancia_str = item_dicionario[0] 
        try:
            nome_arquivo = os.path.basename(instancia_str)
            numero_str = os.path.splitext(nome_arquivo)[0]
            return int(numero_str)
        except ValueError:
            print(f"Aviso: Não foi possível extrair número de '{instancia_str}'.")
            return float('inf') 
    
    try:
        with open(arq_saida, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=colunas_saida)
            writer.writeheader()
            
            for instancia, dados in sorted(resultados.items(), key=extrair_numero_instancia):
                linha_saida = {
                    'Instância': instancia,
                    'FFF': dados.get('FFF', 'N/A'),
                    'HFF': dados.get('HFF', 'N/A'),
                    'PLI': dados.get('PLI', 'N/A'),
                    'Limite teórico': dados.get('Limite teórico', 'N/A')
                }
                writer.writerow(linha_saida)
        
        print(f"\nArquivo consolidado '{arq_saida}' gerado com sucesso!")

    except IOError as e:
        print(f"Erro ao escrever o arquivo de saída: {e}")

if __name__ == "__main__":
    
    ARQ_LOWER_BOUND = "results/resultados_lower_bound.csv"
    ARQ_HEURISTICAS = "results/resultados_heuristicas.csv"
    ARQ_PLI = "results/resultados_pli.csv"
    
    ARQ_SAIDA_CONSOLIDADO = "results/resultados_consolidados.csv"
    
    consolidar_resultados(ARQ_LOWER_BOUND, ARQ_HEURISTICAS, ARQ_PLI, ARQ_SAIDA_CONSOLIDADO)