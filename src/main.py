import sys
from carrega_json import carregar_instancia_json
from heuristica_fff import heuristica_fff
from heuristica_hff import heuristica_hff

if __name__ == "__main__":
    
    # METODO = "FFF" 
    METODO = "HFF"

    nome_arquivo_instancia = "in/650.json"
    
    print(f"Iniciando resolvedor 2D-BPP com Heurística {METODO}...")
    
    dados_carregados = carregar_instancia_json(nome_arquivo_instancia)
    
    if dados_carregados and dados_carregados[3]:
        l_cont, a_cont, max_cont, lista_itens = dados_carregados
        
        containers_usados = []
        if METODO == "FFF":
            containers_usados = heuristica_fff(l_cont, a_cont, max_cont, lista_itens)
        elif METODO == "HFF":
            containers_usados = heuristica_hff(l_cont, a_cont, max_cont, lista_itens)
        
        print("-" * 30)
        print(f"Total de Containers usados ({METODO}): {len(containers_usados)}")
        print("-" * 30)

    else:
        print("Nenhum dado ou item para processar.")