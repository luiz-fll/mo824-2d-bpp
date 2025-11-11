import math
from carrega_json import carregar_instancia_json

def calcular_lower_bound(l_container, a_container, itens):
    """
    Calcula o limite inferior teórico (Lower Bound L1) baseada na área.
    Retorna o número mínimo de containers necessários se o empacotamento fosse perfeito (sem espaços vazios).
    """
    area_bin = l_container * a_container
    area_total_itens = sum(item.largura * item.altura for item in itens)
    
    return math.ceil(area_total_itens / area_bin)

if __name__ == "__main__":
    nome_arquivo = "in/5.json"
    dados = carregar_instancia_json(nome_arquivo)
    
    if dados:
        l_cont, a_cont, max_cont, itens = dados
        lb = calcular_lower_bound(l_cont, a_cont, itens)
        
        print(f"Mínimo teórico de containers (Lower Bound): {lb}")