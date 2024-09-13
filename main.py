from collections import deque

# Algoritmo de Ford-Fulkerson
def ford_fulkerson(grafo, origem, destino):
    def busca_largura(grafo_residual, caminho):
        visitados = set()
        fila = deque([origem])
        visitados.add(origem)

        while fila:
            u = fila.popleft()

            for v in grafo_residual[u]:
                if v not in visitados and grafo_residual[u][v] > 0:  # Se houver capacidade residual
                    fila.append(v)
                    visitados.add(v)
                    caminho[v] = u
                    if v == destino:
                        return True
        return False

    # Construir o grafo residual
    grafo_residual = {u: {} for u in grafo}
    for u in grafo:
        for v in grafo[u]:
            grafo_residual[u][v] = grafo[u][v]
            if v not in grafo_residual:
                grafo_residual[v] = {}
            if u not in grafo_residual[v]:
                grafo_residual[v][u] = 0

    caminho = {}  # Array para armazenar o caminho aumentante
    fluxo_maximo = 0  # Inicializa o fluxo máximo

    # Enquanto existir um caminho aumentante no grafo residual
    while busca_largura(grafo_residual, caminho):
        fluxo_caminho = float('Inf')
        s = destino
        while s != origem:
            fluxo_caminho = min(fluxo_caminho, grafo_residual[caminho[s]][s])
            s = caminho[s]

        # Atualizar as capacidades residuais das arestas e arestas reversas ao longo do caminho
        v = destino
        while v != origem:
            u = caminho[v]
            grafo_residual[u][v] -= fluxo_caminho
            grafo_residual[v][u] += fluxo_caminho
            v = u

        fluxo_maximo += fluxo_caminho
        print(f"Fluxo do caminho: {fluxo_caminho}, fluxo máximo: {fluxo_maximo}")

    return fluxo_maximo

# Algoritmo de Sucessivos Caminhos Mínimos (ASCM)
def ascm(grafo, demanda):
    def dijkstra(grafo_residual, origem, destino, potenciais):
        import heapq

        distancias = {no: float('Inf') for no in grafo_residual}
        distancias[origem] = 0
        caminho = {no: None for no in grafo_residual}
        fila_prioridade = [(0, origem)]

        while fila_prioridade:
            d, u = heapq.heappop(fila_prioridade)

            if d > distancias[u]:
                continue

            for v, (capacidade, custo) in grafo_residual[u].items():
                if capacidade > 0:
                    nova_distancia = distancias[u] + custo + potenciais[u] - potenciais[v]
                    if nova_distancia < distancias[v]:
                        distancias[v] = nova_distancia
                        caminho[v] = u
                        heapq.heappush(fila_prioridade, (nova_distancia, v))

        return caminho if distancias[destino] != float('Inf') else None, distancias

    # Construir o grafo residual
    grafo_residual = {u: {} for u in grafo}
    for u in grafo:
        for v in grafo[u]:
            capacidade, custo = grafo[u][v]
            grafo_residual[u][v] = [capacidade, custo]
            if v not in grafo_residual:
                grafo_residual[v] = {}
            if u not in grafo_residual[v]:
                grafo_residual[v][u] = [0, -custo]

    origem = 'S'
    destino = 'T'
    potenciais = {no: 0 for no in grafo_residual}
    custo_total = 0
    fluxo_total = 0

    while True:
        caminho, distancias = dijkstra(grafo_residual, origem, destino, potenciais)

        if not caminho:
            break

        for no in potenciais:
            if distancias[no] < float('Inf'):
                potenciais[no] += distancias[no]

        fluxo_caminho = float('Inf')
        v = destino
        while v != origem:
            u = caminho[v]
            fluxo_caminho = min(fluxo_caminho, grafo_residual[u][v][0])
            v = u

        v = destino
        while v != origem:
            u = caminho[v]
            grafo_residual[u][v][0] -= fluxo_caminho
            grafo_residual[v][u][0] += fluxo_caminho
            custo_total += fluxo_caminho * grafo_residual[u][v][1]
            v = u

        fluxo_total += fluxo_caminho
        print(f"Fluxo do caminho: {fluxo_caminho}, fluxo total: {fluxo_total}, custo total: {custo_total}")

        if fluxo_total >= demanda[destino]:
            break

    return fluxo_total, custo_total

def main():
    # Grafo para Ford-Fulkerson
    grafo_ford_fulkerson = { 
        "S": {"1" : 10},
        "1": {"2" : 7, "3": 3},
        "2" : {"4" : 3},
        "3" : {"2": 3, "4": 3},
        "4" : {"T": 7}
    }

    # Grafo para Sucessivos Caminhos Mínimos (ASCM)
    grafo_scm = {
        "S": {"1" : (1, 2)},
        "1": {"2" : (2, 1), "3": (3, 1), "4": (5, 2)},
        "2" : {"4" : (2, 1)},
        "3" : {"4": (3, 1)},
        "4" : {"T": (1, 2)}
    }
    
    demanda = { 
        "S": -2,  # Fornece 2 de fluxo
        "T": 2    # Recebe 2 de fluxo
    }
    
    print("\n--- Ford-Fulkerson ---")
    fluxo_maximo = ford_fulkerson(grafo_ford_fulkerson, "S", "T")
    print("\nFord-Fulkerson Fluxo Máximo: ", fluxo_maximo)

    print("\n--- ASCM ---")
    fluxo, custo = ascm(grafo_scm, demanda)
    print("\nASCM Fluxo:", fluxo, " Custo: ", custo)
    
if __name__ == "__main__":
    main()
