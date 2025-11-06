from estrutura import Retangulo

class ContainerFFF:
    """
    Implementação do Container para a heurística FFF (pontos de inserção).
    """
    def __init__(self, id, largura_max, altura_max):
        self.id = id
        self.largura_max = largura_max
        self.altura_max = altura_max
        self.itens_empacotados = [] 
        self.posicoes_itens = [] 
        self.pontos_insercao = [(0, 0)]

    def __repr__(self):
        return f"ContainerFFF(id={self.id}, itens={len(self.itens_empacotados)})"

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
                novo_container = ContainerFFF(id=novo_id, 
                                             largura_max=l_container, 
                                             altura_max=a_container)
                
                if novo_container.tentar_empacotar_item(item):
                    containers_usados.append(novo_container)
                    item_alocado = True
    
    return containers_usados