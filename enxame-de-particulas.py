import numpy as np
import math
import time

# Função para ler o arquivo TSPLIB
def ler_pontos_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    
    pontos = {}
    for linha in linhas:
        partes = linha.split()
        id_ponto = int(partes[0])
        x = float(partes[1])
        y = float(partes[2])
        pontos[id_ponto] = (x, y)
    
    return pontos

# Função para calcular distância
def distancia(coord1, coord2):
    xi, yi = coord1
    xj, yj = coord2
    xd = xi - xj
    yd = yi - yj
    dij = round(math.sqrt(xd**2 + yd**2))  
    return dij

# Função para definir a distância da rota
def custo_rota(rota, pontos):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += distancia(pontos[rota[i]], pontos[rota[i + 1]])
    distancia_total += distancia(pontos[rota[-1]], pontos[rota[0]])
    return distancia_total

# Função para criar novas rotas com inversão
def inverter(rota):
    nova_rota = np.array(rota)
    i, j = np.random.choice(len(nova_rota), size=2, replace=False)
    if i > j:
        i, j = j, i  
    nova_rota[i:j+1] = np.flip(nova_rota[i:j+1])
    return nova_rota.tolist()

# Algoritmo do vizinho mais próximo
def algoritmo_vizinho_mais_proximo(pontos):
    ids_pontos = list(pontos.keys())
    ponto_inicial = np.random.choice(ids_pontos)
    caminho = [ponto_inicial]
    distancia_total = 0

    while len(caminho) < len(ids_pontos):
        ultimo_ponto = caminho[-1]
        menor_distancia = float('inf')
        melhor_ponto = None

        for ponto in ids_pontos:
            if ponto not in caminho:
                dist = distancia(pontos[ultimo_ponto], pontos[ponto])
                if dist < menor_distancia:
                    menor_distancia = dist
                    melhor_ponto = ponto

        caminho.append(melhor_ponto)
        distancia_total += menor_distancia

    distancia_total += distancia(pontos[caminho[-1]], pontos[caminho[0]])
    return caminho, distancia_total

# Função principal enxame                                #tolerancia de quantas rotas nao tiveram nenhuma melhoria
def enxame(pontos, num_particulas=100, max_iter=5000, tolerancia=1000, i_inter=500): #iteracoes para poder aplicar o vizinho mais proximo
    ids_pontos = list(pontos.keys())
    particulas = [np.random.permutation(ids_pontos).tolist() for _ in range(num_particulas)]
    rotas_verificadas = set(tuple(p) for p in particulas)
    #lista para verificar se uma rota ja foi analisada

    melhor_custo_local = [custo_rota(rota, pontos) for rota in particulas]
    melhor_rota_global = particulas[0]
    melhor_custo_global = custo_rota(melhor_rota_global, pontos)
     #criacao da lista de particulas aleatoriamentes juntamente com as variaveis para auxiliar a atualização das posições
    c = 0
    
    # Loop sobre as iterações
    for iteracao in range(max_iter):
        if c >= tolerancia:
            break
        
        #tolerancia de quantas rotas nao tiveram nenhuma melhoria
        if iteracao % i_inter == 0:
            for i in range(num_particulas // 2):    #aplicar o vizinho mais próximo em metade das particulas, mantendo equilibrio entre diversidade para explorar e refinamento
                rota_otimizada, custo_otimizado = algoritmo_vizinho_mais_proximo(pontos)
                if custo_otimizado < melhor_custo_local[i]: #verificacao da rota nova localmente
                    particulas[i] = rota_otimizada
                    melhor_custo_local[i] = custo_otimizado
                    c = 0

                if custo_otimizado < melhor_custo_global: #verificacao da rota nova globalmente
                    melhor_rota_global = rota_otimizada
                    melhor_custo_global = custo_otimizado
                    c = 0

       #loop sobre as particulas para misturar a array
        for i in range(num_particulas):
            nova_rota = inverter(particulas[i])
            if tuple(nova_rota) not in rotas_verificadas: #verificacao se ja foi vista
                rotas_verificadas.add(tuple(nova_rota))
                custo_atual = custo_rota(nova_rota, pontos) #atualizacao do custo atual para verificar com o melhor local e global
                if custo_atual < melhor_custo_local[i]: #verificacao local 
                    particulas[i] = nova_rota
                    melhor_custo_local[i] = custo_atual
                    c = 0
                else:
                    c += 1 #se nao for melhor adiciona um no contador, ou seja nao melhorou nada o melhor custo local
                
                if custo_atual < melhor_custo_global: #verificacao global
                    melhor_rota_global = nova_rota
                    melhor_custo_global = custo_atual
                    c = 0

    return melhor_rota_global, melhor_custo_global

def main():
    inicio_tempo = time.time()
    pontos = ler_pontos_arquivo('pontos.txt')
    rota, distancia = enxame(pontos)
    fim_tempo = time.time()
    tempo_execucao = fim_tempo - inicio_tempo
    print("Melhor rota:", rota)
    print("Menor distância:", f"{float(distancia)}")
    print(f"Tempo de execução: {tempo_execucao:.2f} segundos")
    
if __name__ == "__main__":
    main()
