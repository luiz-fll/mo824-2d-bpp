class ContainerFFF:
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
        # (Sua implementação atual está correta, mantenha-a)
        if (x + novo_item.largura > self.largura_max) or (y + novo_item.altura > self.altura_max):
            return True
        for i, item_existente in enumerate(self.itens_empacotados):
            pos_x, pos_y = self.posicoes_itens[i]
            # Verifica interseção de retângulos
            if (x < pos_x + item_existente.largura and x + novo_item.largura > pos_x and
                y < pos_y + item_existente.altura and y + novo_item.altura > pos_y):
                return True
        return False

    def adicionar_item(self, item, x, y):
        """
        Adiciona um item em uma posição específica e atualiza os pontos.
        Usado tanto para empacotamento normal quanto para reconstrução.
        """
        self.itens_empacotados.append(item)
        self.posicoes_itens.append((x, y))
        
        if (x, y) in self.pontos_insercao:
            self.pontos_insercao.remove((x, y))
            
        novo_ponto_direita = (x + item.largura, y)
        novo_ponto_acima = (x, y + item.altura)
        
        if novo_ponto_direita not in self.pontos_insercao and \
           novo_ponto_direita[0] < self.largura_max and \
           novo_ponto_direita[1] < self.altura_max:
            self.pontos_insercao.append(novo_ponto_direita)
            
        if novo_ponto_acima not in self.pontos_insercao and \
           novo_ponto_acima[0] < self.largura_max and \
           novo_ponto_acima[1] < self.altura_max:
            self.pontos_insercao.append(novo_ponto_acima)
            
        self.pontos_insercao.sort(key=lambda p: (p[1], p[0])) # Ordena por Y, depois X

    def tentar_empacotar_item(self, item):
        for (x, y) in self.pontos_insercao:
            if not self.verifica_sobreposicao(item, x, y):
                self.adicionar_item(item, x, y)
                return True
        return False

    def remover_item_pelo_id(self, id_item):
        """
        Remove um item e reconstrói o estado do container do zero
        para garantir que os pontos de inserção estejam corretos.
        """
        encontrou = False
        for i, item in enumerate(self.itens_empacotados):
            if item.id == id_item:
                self.itens_empacotados.pop(i)
                self.posicoes_itens.pop(i)
                encontrou = True
                break
        
        if encontrou:
            # Reconstrói o estado interno
            itens_restantes = list(self.itens_empacotados)
            posicoes_restantes = list(self.posicoes_itens)
            
            # Reseta
            self.itens_empacotados = []
            self.posicoes_itens = []
            self.pontos_insercao = [(0, 0)]
            
            # Reinsere tudo nas mesmas posições
            for i, item in enumerate(itens_restantes):
                self.adicionar_item(item, posicoes_restantes[i][0], posicoes_restantes[i][1])
            return True
            
        return False

def heuristica_fff(l_container, a_container, max_containers, itens):
    for item in itens:
        if item.largura > l_container or item.altura > a_container:
            print(f"ERRO: Item {item.id} (L:{item.largura}, A:{item.altura}) não cabe no container (L:{l_container}, A:{a_container})")
            return None

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