import sys
import json

class Retangulo:
    def __init__(self, id, largura, altura):
        self.id = id
        self.largura = largura
        self.altura = altura


class Container:
    def __init__(self, id, largura_max, altura_max):
        self.id = id
        self.largura_max = largura_max
        self.altura_max = altura_max
        self.itens_empacotados = [] 
        self.posicoes_itens = [] 
        self.pontos_insercao = [(0, 0)]

    def verifica_sobreposicao(self, novo_item, x, y):
        if (x + novo_item.largura > self.largura_max) or (y + novo_item.altura > self.altura_max):
            return True 
        for i, item_existente in enumerate(self.itens_empacotados):
            pos_x, pos_y = self.posicoes_itens[i]
            nx1, ny1 = x, y
            nx2, ny2 = x + novo_item.largura, y + novo_item.altura
            ex1, ey1 = pos_x, pos_y
            ex2, ey2 = pos_x + item_existente.largura, pos_y + item_existente.altura
            cruza_x = (nx1 < ex2) and (nx2 > ex1)
            cruza_y = (ny1 < ey2) and (ny2 > ey1)
            if cruza_x and cruza_y:
                return True 
        return False 

    def adicionar_item(self, item, x, y):
        self.itens_empacotados.append(item)
        self.posicoes_itens.append((x, y))
        self.pontos_insercao.remove((x, y))
        novo_ponto_direita = (x + item.largura, y)
        novo_ponto_acima = (x, y + item.altura)
        if novo_ponto_direita not in self.pontos_insercao:
            self.pontos_insercao.append(novo_ponto_direita)
        if novo_ponto_acima not in self.pontos_insercao:
            self.pontos_insercao.append(novo_ponto_acima)
        self.pontos_insercao.sort(key=lambda p: (p[1], p[0])) 

    def tentar_empacotar_item(self, item):
        for (x, y) in self.pontos_insercao:
            if not self.verifica_sobreposicao(item, x, y):
                self.adicionar_item(item, x, y)
                return True 
        return False 

def carregar_instancia_json(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data.get('Objects') or len(data['Objects']) == 0:
            print("Erro: JSON não contém a chave 'Objects' ou 'Objects' está vazio.")
            sys.exit(1)
            
        container_info = data['Objects'][0]
        l_container = container_info['Length']
        a_container = container_info['Height']
        
        max_containers = sys.maxsize 
        
        itens = []
        item_id_counter = 1
        if not data.get('Items'):
            print("Erro: JSON não contém a chave 'Items'.")
            sys.exit(1)
            
        for item_tipo in data['Items']:
            l_item = item_tipo['Length']
            a_item = item_tipo['Height']
            demanda = item_tipo.get('Demand', 1) 
            
            for _ in range(demanda):
                itens.append(Retangulo(id=item_id_counter, 
                                       largura=l_item, 
                                       altura=a_item))
                item_id_counter += 1
        
        print(f"Instância '{data.get('Name', nome_arquivo)}' carregada com sucesso.")
        print(f"Dimensões do Container: {l_container}x{a_container}")
        print(f"Total de Itens (considerando a demanda): {len(itens)}")
        
        return l_container, a_container, max_containers, itens

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{nome_arquivo}' não é um JSON válido.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        sys.exit(1)


def heuristica_fff(l_container, a_container, max_containers, itens):
    itens.sort(key=lambda item: (item.altura, item.largura), reverse=True)
    containers_usados = []
    for i, item in enumerate(itens):
        item_alocado = False
        
        for container in containers_usados:
            if container.tentar_empacotar_item(item):
                item_alocado = True
                break 
        
        if not item_alocado:
            if len(containers_usados) < max_containers:
                novo_id = len(containers_usados) + 1
                novo_container = Container(id=novo_id, 
                                           largura_max=l_container, 
                                           altura_max=a_container)
                
                if novo_container.tentar_empacotar_item(item):
                    containers_usados.append(novo_container)
                    item_alocado = True
            
    return containers_usados


if __name__ == "__main__":
    nome_arquivo_instancia = "in/650.json"
    
    dados_carregados = carregar_instancia_json(nome_arquivo_instancia)
    
    if dados_carregados and dados_carregados[3]:
        l_cont, a_cont, max_cont, lista_itens = dados_carregados
        containers_usados = heuristica_fff(l_cont, a_cont, max_cont, lista_itens)
        print(f"Total de Containers usados: {len(containers_usados)}")
    else:
        print("Nenhum dado ou item para processar.")