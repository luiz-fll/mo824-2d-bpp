import carrega_json
import time

class GRASP:
    """
    Classe que implementa a metaheurística GRASP.
    """
    def __init__(self, iteracoes_max, tempo_max):
        self.iteracoes_max = iteracoes_max
        self.tempo_max = tempo_max
        self.melhor_solucao = None
        self.tempo_inicio = None

    def construir_solucao(self, l_container, a_container, max_containers, itens):
        """
        Utiliza uma variação do FFDH ou FFF, mas com um elemento de aleatoriedade, 
        selecionando itens a partir de uma Lista Restrita de Candidatos (RCL), em
        vez de uma escolha puramente gulosa
        """
        # monitorar tempo
        # implementar estrategias de diversificação/intensificação?
        pass
    
    def procurar_vizinho_melhor(self, solucao):
        """
        Aplica movimentos de perturbação no arranjo de itens (ex: troca de posição de 
        dois itens dentro de um bin, ou realocação de itens entre bins) para escapar
        de ótimos locais.
        """
        # monitorar tempo
        # best-improving ou first-improving?
        pass

    def busca_local(self, solucao):
        melhor_vizinho = self.procurar_vizinho_melhor(solucao)
        while len(melhor_vizinho) < len(solucao) and time.time() - self.tempo_inicio < self.tempo_max:
            solucao = melhor_vizinho
            melhor_vizinho = self.procurar_vizinho_melhor(solucao)

        return solucao     

    def atualizar_solucao(self, solucao):
        if len(self.melhor_solucao) > len(solucao):
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
