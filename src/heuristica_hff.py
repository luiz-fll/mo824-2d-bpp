class Level:
    def __init__(self, altura, max_largura):
        self.altura = altura
        self.max_largura = max_largura
        self.largura_ocupada = 0
        self.itens = []

    def tentar_adicionar_item(self, item):
        if item.altura > self.altura:
            return False
        if (self.largura_ocupada + item.largura) > self.max_largura:
            return False
        
        self.itens.append(item)
        self.largura_ocupada += item.largura
        return True
    
    def remover_item_pelo_id(self, id_item):
        for i, item in enumerate(self.itens):
            if item.id == id_item:
                self.itens.pop(i)
                self.largura_ocupada -= item.largura
                return True
        return False

    def __repr__(self):
        return f"Level(h={self.altura}, w_usada={self.largura_ocupada}/{self.max_largura}, itens={len(self.itens)})"

class ContainerHFF:
    def __init__(self, id, largura_max, altura_max):
        self.id = id
        self.largura_max = largura_max
        self.altura_max = altura_max
        self.altura_ocupada = 0
        self.levels = []

    def altura_disponivel(self):
        return self.altura_max - self.altura_ocupada
    
    def remover_item_pelo_id(self, id_item):
        for i, level in enumerate(self.levels):
            if level.remover_item_pelo_id(id_item):
                if len(level.itens) == 0:
                    self.levels.pop(i)
                    self.altura_ocupada -= level.altura
                return True
        return False

    def tentar_adicionar_level(self, level):
        if level.altura > self.altura_disponivel():
            return False
        
        self.levels.append(level)
        self.altura_ocupada += level.altura
        return True
    
    def __repr__(self):
        return f"ContainerHFF(id={self.id}, h_usada={self.altura_ocupada}/{self.altura_max}, levels={len(self.levels)})"


def heuristica_hff(l_container, a_container, max_containers, itens):
    itens.sort(key=lambda item: item.altura, reverse=True)
    
    itens_restantes = list(itens)
    containers_usados = []

    while itens_restantes and len(containers_usados) < max_containers:
        
        novo_id = len(containers_usados) + 1
        container_atual = ContainerHFF(id=novo_id, 
                                       largura_max=l_container, 
                                       altura_max=a_container)
        containers_usados.append(container_atual)
        
        while True:
            
            primeiro_item_idx = -1
            for i, item in enumerate(itens_restantes):
                if item.altura <= container_atual.altura_disponivel():
                    primeiro_item_idx = i
                    break
            
            if primeiro_item_idx == -1:
                break
                
            primeiro_item = itens_restantes.pop(primeiro_item_idx)
            novo_level = Level(altura=primeiro_item.altura, max_largura=l_container)
            novo_level.tentar_adicionar_item(primeiro_item)
            
            for i in range(len(itens_restantes) - 1, -1, -1):
                item_candidato = itens_restantes[i]
                
                if novo_level.tentar_adicionar_item(item_candidato):
                    itens_restantes.pop(i)

            if not container_atual.tentar_adicionar_level(novo_level):
                itens_restantes.insert(primeiro_item_idx, primeiro_item) 
                break 

    return containers_usados