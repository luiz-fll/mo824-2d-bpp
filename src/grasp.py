import carrega_json
import time
import random
from heuristica_fff import ContainerFFF
from heuristica_hff import ContainerHFF, Level

class GRASP:
    """
    Classe que implementa a metaheurística GRASP.
    """
    def __init__(self, iteracoes_max, tempo_max, estrategia_construcao="fff", estrategia_busca="first_improving", alpha=0.3):
        self.iteracoes_max = iteracoes_max
        self.tempo_max = tempo_max
        self.melhor_solucao = None
        self.tempo_inicio = None
        self.estrategia_construcao = estrategia_construcao
        self.estrategia_busca = estrategia_busca
        self.alpha = alpha

    def heuristica_fff_rcl(self, l_container, a_container, max_containers, itens):
        """
        Variante da FFF com Lista Restrita de Candidatos (RCL).
        """
        itens_restantes = list(itens)
        containers_usados = []

        while itens_restantes and time.time() - self.tempo_inicio < self.tempo_max:
            areas = [item.largura * item.altura for item in itens_restantes]
            melhor = max(areas)
            pior = min(areas)
            limite = melhor - self.alpha * (melhor - pior)

            rcl = [itens_restantes[i] for i, m in enumerate(areas) if m >= limite]

            item_escolhido = random.choice(rcl)
            itens_restantes.remove(item_escolhido)

            item_alocado = False
            for container in containers_usados:
                if container.tentar_empacotar_item(item_escolhido):
                    item_alocado = True
                    break

            if not item_alocado:
                if len(containers_usados) < max_containers:
                    novo_id = len(containers_usados) + 1
                    novo_container = ContainerFFF(id=novo_id,
                                                largura_max=l_container,
                                                altura_max=a_container)
                    if novo_container.tentar_empacotar_item(item_escolhido):
                        containers_usados.append(novo_container)

        return containers_usados
    
    def heuristica_hff_rcl(self, l_container, a_container, max_containers, itens):
        """
        Variante da HFF com Lista Restrita de Candidatos (RCL).
        """
        itens_restantes = list(itens)
        containers_usados = []

        while itens_restantes and len(containers_usados) < max_containers and time.time() - self.tempo_inicio < self.tempo_max:
            novo_id = len(containers_usados) + 1
            container_atual = ContainerHFF(id=novo_id,
                                        largura_max=l_container,
                                        altura_max=a_container)
            containers_usados.append(container_atual)

            while time.time() - self.tempo_inicio < self.tempo_max:
                candidatos_validos = [it for it in itens_restantes
                                    if it.altura <= container_atual.altura_disponivel()]
                if not candidatos_validos:
                    break

                alturas = [it.altura for it in candidatos_validos]
                melhor = max(alturas)
                pior = min(alturas)
                limite = melhor - self.alpha * (melhor - pior)
                rcl = [it for it in candidatos_validos if it.altura >= limite]

                if not rcl:
                    break

                item_escolhido = random.choice(rcl)
                itens_restantes.remove(item_escolhido)

                novo_level = Level(altura=item_escolhido.altura, max_largura=l_container)
                novo_level.tentar_adicionar_item(item_escolhido)

                for i in range(len(itens_restantes) - 1, -1, -1):
                    item_candidato = itens_restantes[i]
                    if novo_level.tentar_adicionar_item(item_candidato):
                        itens_restantes.pop(i)

                if not container_atual.tentar_adicionar_level(novo_level):
                    itens_restantes.append(item_escolhido)
                    break

        return containers_usados

    def construir_solucao(self, l_container, a_container, max_containers, itens):
        """
        Utiliza uma variação do FFDH ou FFF, mas com um elemento de aleatoriedade, 
        selecionando itens a partir de uma Lista Restrita de Candidatos (RCL), em
        vez de uma escolha puramente gulosa
        """
        # monitorar tempo
        # implementar estrategias de diversificação/intensificação?
        if self.estrategia_construcao == "fff":
            return self.heuristica_fff_rcl(l_container, a_container, max_containers, itens)
        if self.estrategia_construcao == "hff":
            return self.heuristica_hff_rcl(l_container, a_container, max_containers, itens)
                
    
    def vizinho_first_improving(self, solucao):
        melhor = solucao
        melhor_custo = len(solucao)

        for i, c1 in enumerate(solucao):
            for j, item in enumerate(list(c1.itens_empacotados)):
                for k, c2 in enumerate(solucao):
                    if time.time() - self.tempo_inicio > self.tempo_max:
                        return melhor
                    if i == k:
                        continue
                    # tenta mover o item de c1 para c2
                    c1.itens_empacotados.pop(j)
                    if c2.tentar_empacotar_item(item):
                        # remove c1 vazio
                        nova_solucao = [c for c in solucao if c.itens_empacotados]
                        if len(nova_solucao) < melhor_custo:
                            return nova_solucao  # first improving
                    # rollback
                    c1.itens_empacotados.insert(j, item)
        return melhor
    
    def vizinho_best_improving(self, solucao):
        melhor = solucao
        melhor_custo = len(solucao)

        for i, c1 in enumerate(solucao):
            for j, item in enumerate(list(c1.itens_empacotados)):
                for k, c2 in enumerate(solucao):
                    if time.time() - self.tempo_inicio < self.tempo_max:
                        return melhor
                    if i == k:
                        continue
                    # tenta mover o item de c1 para c2
                    c1.itens_empacotados.pop(j)
                    if c2.tentar_empacotar_item(item):
                        # remove c1 vazio
                        nova_solucao = [c for c in solucao if c.itens_empacotados]
                        novo_custo = len(nova_solucao)
                        if novo_custo < melhor_custo:
                            melhor = nova_solucao
                            melhor_custo = novo_custo
                    # rollback
                    c1.itens_empacotados.insert(j, item)
        return melhor

    def procurar_vizinho_melhor(self, solucao):
        """
        Aplica movimentos de perturbação no arranjo de itens (ex: troca de posição de 
        dois itens dentro de um bin, ou realocação de itens entre bins) para escapar
        de ótimos locais.
        """
        # monitorar tempo
        # best-improving ou first-improving?
        if self.estrategia_busca == "first_improving":
            return self.vizinho_first_improving(solucao)
        if self.estrategia_busca == "best_improving":
            return self.vizinho_best_improving(solucao)

    def busca_local(self, solucao):
        melhor_vizinho = self.procurar_vizinho_melhor(solucao)
        while len(melhor_vizinho) < len(solucao) and time.time() - self.tempo_inicio < self.tempo_max:
            solucao = melhor_vizinho
            melhor_vizinho = self.procurar_vizinho_melhor(solucao)

        return solucao     

    def atualizar_solucao(self, solucao):
        if self.melhor_solucao is None:
            self.melhor_solucao = solucao
        elif len(self.melhor_solucao) > len(solucao):
            self.melhor_solucao = solucao

    def executar(self, caminho_instancia):
        self.tempo_inicio = time.time()
        l_container, a_container, max_containers, itens = carrega_json.carregar_instancia_json(caminho_instancia)

        iteracoes = 0
        while iteracoes < self.iteracoes_max and time.time() - self.tempo_inicio < self.tempo_max:
            solucao = self.construir_solucao(l_container, a_container, max_containers, itens)
            solucao = self.busca_local(solucao)
            self.atualizar_solucao(solucao)
            iteracoes += 1

        return self.melhor_solucao


if __name__ == "__main__":
    nome_arquivo_instancia = "in/650.json"

    grasp = GRASP(1000, 10)
    sol = grasp.executar(nome_arquivo_instancia)
    print(f"Solução:{sol}")
    print(f"Bins:{len(sol)}")
    print(f"Tempo:{time.time() - grasp.tempo_inicio} s")