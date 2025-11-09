import copy
import time
import random

from carrega_json import carregar_instancia_json
from heuristica_fff import ContainerFFF
from heuristica_hff import ContainerHFF, Level

class GRASP:
    """
    Classe que implementa a metaheurística GRASP.
    """
    def __init__(self, iteracoes_max, tempo_max, estrategia_construcao="hff", estrategia_busca="best_improving", alpha=0.2, limite_sem_melhora=20):
        self.iteracoes_max = iteracoes_max
        self.tempo_max = tempo_max
        self.estrategia_construcao = estrategia_construcao.lower()
        self.estrategia_busca = estrategia_busca.lower()
        
        self.alpha = alpha
        self.iteracoes_sem_melhora = 0
        self.limite_sem_melhora = limite_sem_melhora

        self.melhor_solucao = None
        self.melhor_custo = float('inf')
        self.tempo_inicio = None

    def _calcular_ocupacao(self, container):
        """Calcula a área total ocupada por itens em um container."""
        area_total = 0
        if isinstance(container, ContainerFFF):
            for item in container.itens_empacotados:
                area_total += item.largura * item.altura
        elif isinstance(container, ContainerHFF):
            for lvl in container.levels:
                for item in lvl.itens:
                    area_total += item.largura * item.altura
        return area_total

    def _funcao_objetivo_secundaria(self, solucao):
        """
        Calcula a soma dos quadrados das ocupações dos containers.
        Quanto maior, melhor (significa containers mais desbalanceados: uns muito cheios, outros vazios).
        """
        f_sec = 0
        for container in solucao:
            ocupacao = self._calcular_ocupacao(container)
            f_sec += ocupacao ** 2
        return f_sec
    
    def _get_custo(self, solucao):
        return (len(solucao), -self._funcao_objetivo_secundaria(solucao))

    def _get_itens(self, container):
        """Retorna lista plana de itens de qualquer tipo de container."""
        if isinstance(container, ContainerFFF):
            return list(container.itens_empacotados)
        elif isinstance(container, ContainerHFF):
            return [item for lvl in container.levels for item in lvl.itens]
        return []

    def _remover_item_container(self, container, item_alvo):
        """Remove um item de um container (FFF ou HFF) e atualiza seus estados."""
        if isinstance(container, ContainerFFF):
            container.itens_empacotados = [it for it in container.itens_empacotados if it.id != item_alvo.id]
        
        elif isinstance(container, ContainerHFF):
            for i_lvl, lvl in enumerate(container.levels):
                tam_antes = len(lvl.itens)
                lvl.itens = [it for it in lvl.itens if it.id != item_alvo.id]
                
                if len(lvl.itens) < tam_antes:
                    lvl.largura_ocupada -= item_alvo.largura
                    
                    if len(lvl.itens) == 0:
                        container.altura_ocupada -= lvl.altura
                        container.levels.pop(i_lvl)
                    break

    def _adicionar_item_container(self, container, item):
        if isinstance(container, ContainerFFF):
            return container.tentar_empacotar_item(item)
        elif isinstance(container, ContainerHFF):
            for lvl in container.levels:
                if lvl.tentar_adicionar_item(item):
                    return True
            if item.altura <= container.altura_disponivel():
                novo_lvl = Level(item.altura, container.largura_max)
                novo_lvl.tentar_adicionar_item(item)
                return container.tentar_adicionar_level(novo_lvl)
            return False
        return False

    def heuristica_fff_rcl(self, l_c, a_c, max_c, itens):
        """FFF Aleatorizado usando apenas ALTURA como critério (FFDH-RCL)."""
        itens_restantes = list(itens)
        containers_usados = []

        while itens_restantes:
            criterios = [item.altura for item in itens_restantes]
            melhor, pior = max(criterios), min(criterios)
            limite = melhor - self.alpha * (melhor - pior)

            rcl = [itens_restantes[i] for i, c in enumerate(criterios) if c >= limite]
            item_escolhido = random.choice(rcl)
            itens_restantes.remove(item_escolhido)

            item_alocado = False
            for container in containers_usados:
                if container.tentar_empacotar_item(item_escolhido):
                    item_alocado = True
                    break
            if not item_alocado and len(containers_usados) < max_c:
                novo_c = ContainerFFF(len(containers_usados)+1, l_c, a_c)
                if novo_c.tentar_empacotar_item(item_escolhido):
                    containers_usados.append(novo_c)
                    item_alocado = True
            

        return containers_usados

    def heuristica_hff_rcl(self, l_container, a_container, max_containers, itens):
        """Fase construtiva HFF aleatorizada (baseada em altura)."""
        itens_restantes = list(itens)
        containers_usados = []

        while itens_restantes and len(containers_usados) < max_containers:
            cont_atual = ContainerHFF(len(containers_usados) + 1, l_container, a_container)
            containers_usados.append(cont_atual)

            while True:
                # Filtra apenas itens que cabem na altura restante do container atual
                candidatos = [it for it in itens_restantes if it.altura <= cont_atual.altura_disponivel()]
                if not candidatos:
                    break # Container cheio (verticalmente)

                # RCL baseada na ALTURA (padrão para level packing)
                alturas = [it.altura for it in candidatos]
                melhor, pior = max(alturas), min(alturas)
                limite = melhor - self.alpha * (melhor - pior)
                rcl = [it for it in candidatos if it.altura >= limite]

                if not rcl: break
                
                # Escolhe item para iniciar um novo nível
                item_escolhido = random.choice(rcl)
                itens_restantes.remove(item_escolhido)

                novo_level = Level(item_escolhido.altura, l_container)
                novo_level.tentar_adicionar_item(item_escolhido)

                # Preenche o resto do nível (First-Fit na largura)
                # Aqui pode ser guloso determinístico mesmo, ou também aleatorizado se quiser.
                for i in range(len(itens_restantes) - 1, -1, -1):
                    if novo_level.tentar_adicionar_item(itens_restantes[i]):
                        itens_restantes.pop(i)

                if not cont_atual.tentar_adicionar_level(novo_level):
                    # Não deveria acontecer devido ao filtro 'candidatos', mas por segurança:
                    break 
        
        return containers_usados

    def construir_solucao(self, l_c, a_c, max_c, itens):
        if self.estrategia_construcao == "fff":
            return self.heuristica_fff_rcl(l_c, a_c, max_c, itens)
        elif self.estrategia_construcao == "hff":
            return self.heuristica_hff_rcl(l_c, a_c, max_c, itens)
        raise ValueError("Estratégia de construção desconhecida.")

    def procurar_vizinho(self, solucao):
        """
        Explora a vizinhança 'Shift' aplicando e revertendo movimentos na própria solução.
        """
        # Melhor custo inicial é o da solução atual
        melhor_custo = self._get_custo(solucao)
        # Se for 'best_improving', precisaremos salvar uma cópia da melhor encontrada
        melhor_vizinho_snapshot = None 
        melhorou_algo = False

        tipo_busca = "first" if self.estrategia_busca == "first_improving" else "best"

        for i_origem, c_origem in enumerate(solucao):
            itens_origem = list(self._get_itens(c_origem))
            
            for item in itens_origem:
                if time.time() - self.tempo_inicio > self.tempo_max:
                    return melhor_vizinho_snapshot if melhor_vizinho_snapshot else solucao

                # Loop interno: Container de Destino
                for i_destino, c_destino in enumerate(solucao):
                    if i_origem == i_destino: continue

                    # --- TENTATIVA DE MOVIMENTO (APPLY) ---
                    # 1. Tenta adicionar no destino
                    if self._adicionar_item_container(c_destino, item):
                        c_origem.remover_item_pelo_id(item.id)

                        # 3. Avalia
                        # Precisamos filtrar containers vazios temporariamente para calcular o custo real
                        solucao_temp = [c for c in solucao if len(self._get_itens(c)) > 0]
                        novo_custo = self._get_custo(solucao_temp)

                        if novo_custo < melhor_custo:
                            # ENCONTROU MELHORA
                            melhor_custo = novo_custo
                            melhorou_algo = True
                            
                            if tipo_busca == "first":
                                # Se é first improving, removemos definitivamente os vazios e retornamos
                                # Não precisamos de deepcopy aqui pois vamos retornar essa solução modificada
                                solucao[:] = [c for c in solucao if len(self._get_itens(c)) > 0]
                                return solucao
                            else:
                                # Se é best improving, precisamos salvar esse estado (snapshot)
                                # porque vamos REVERTER para continuar procurando outros vizinhos.
                                melhor_vizinho_snapshot = copy.deepcopy(solucao_temp)

                        # --- REVERSÃO (UNDO) ---
                        # Sempre reverte se não retornou imediatamente (caso do best improving ou falha)
                        c_destino.remover_item_pelo_id(item.id)
                        # Tenta colocar de volta na origem. 
                        # NOTA: Pode não voltar para a EXATA mesma posição se houver múltiplas opções,
                        # mas em heurísticas isso é geralmente aceitável.
                        if not self._adicionar_item_container(c_origem, item):
                             print(f"ERRO CRÍTICO: Não foi possível reverter item {item.id} para container {c_origem.id}")

        if melhorou_algo and melhor_vizinho_snapshot:
             return melhor_vizinho_snapshot
             
        return solucao

    def busca_local(self, solucao_inicial):

        solucao_atual = solucao_inicial
        custo_atual = self._get_custo(solucao_atual)

        while True:
            nova_solucao = self.procurar_vizinho(solucao_atual)
            custo_nova_solucao = self._get_custo(nova_solucao)
            
            if custo_nova_solucao < custo_atual:
                solucao_atual = nova_solucao
                custo_atual = custo_nova_solucao
            else:
                break
        return solucao_atual


    def executar(self, caminho_instancia):
        self.tempo_inicio = time.time()
        l_c, a_c, max_c, itens = carregar_instancia_json(caminho_instancia)

        iteracao = 0
        while iteracao < self.iteracoes_max:
            if time.time() - self.tempo_inicio > self.tempo_max: break
            
            iteracao += 1
            solucao_inicial = self.construir_solucao(l_c, a_c, max_c, itens)
            solucao_refinada = self.busca_local(solucao_inicial)
            
            if self.melhor_solucao is None or len(solucao_refinada) < len(self.melhor_solucao):
                self.melhor_solucao = solucao_refinada
                self.iteracoes_sem_melhora = 0
                print(f"[{time.time()-self.tempo_inicio:.2f}s] Nova melhor solução: {len(self.melhor_solucao)} bins (Iter {iteracao})")
            else:
                self.iteracoes_sem_melhora += 1
                print(f"[{time.time()-self.tempo_inicio:.2f}s] Iterações sem melhora: {self.iteracoes_sem_melhora}")
                
            if self.iteracoes_sem_melhora >= self.limite_sem_melhora:
                self.alpha = min(1.0, self.alpha + 0.1)
                self.iteracoes_sem_melhora = 0


        return self.melhor_solucao, iteracao


if __name__ == "__main__":
    arquivo = "in/650.json" 
    
    grasp = GRASP(iteracoes_max=10000, tempo_max=600, estrategia_construcao="hff", estrategia_busca="first_improving", alpha=0.2)
    
    melhor_sol, iteracao = grasp.executar(arquivo)
    
    print("\n--- FIM DO GRASP ---")
    if melhor_sol:
        print(f"Melhor solução encontrada: {len(melhor_sol)} containers. Total de iterações: {iteracao}")
    else:
        print("Nenhuma solução encontrada.")