import json
import sys
from estrutura import Retangulo 

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