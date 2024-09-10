import time
import math
import numpy as np  # Importando a biblioteca numpy para operações numéricas

# Função para ler e processar os dados de um arquivo de pontos
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

# Função para calcular a distância entre dois pontos
def distancia(i, j, coordenadas):
    xi, yi = coordenadas[i]
    xj, yj = coordenadas[j]

    xd = xi - xj
    yd = yi - yj
    
    dij = round(math.sqrt(xd**2 + yd**2))
    
    return dij

# Função que implementa o algoritmo do vizinho mais próximo para encontrar um caminho aproximado
def vizinho_mais_proximo(percurso, ponto_inicial=None):
    caminho_final = []
    distancia_total = 0
    
    # Gerando um ponto inicial aleatório com numpy se não for fornecido
    if ponto_inicial is None:
        ponto_inicial = np.random.randint(1, len(percurso))
    
    ponto_atual = ponto_inicial
    melhor_ponto = None

    # Executa o loop até que todos os pontos tenham sido visitados
    while len(caminho_final) < len(percurso) - 1:
        menor_distancia = float('inf')
        for i in percurso:  # Itera sobre todos os pontos do percurso
            if i != ponto_atual and i not in caminho_final:  # Verifica se o ponto ainda não foi visitado e não é o atual
                dist = distancia(ponto_atual, i, percurso)  # Calcula a distância entre o ponto atual e o ponto candidato
                if dist < menor_distancia:  # Atualiza a menor distância encontrada e o melhor ponto
                    menor_distancia = dist
                    melhor_ponto = i
        distancia_total += menor_distancia  # Incrementa a distância total com a menor distância encontrada
        caminho_final.append(ponto_atual)  # Adiciona o ponto atual ao caminho final
        ponto_atual = melhor_ponto  # Atualiza o ponto atual para o melhor ponto encontrado
    distancia_total += distancia(ponto_atual, ponto_inicial, percurso)  # Fecha o ciclo ao adicionar a distância de retorno ao ponto inicial
    
    return distancia_total, ponto_inicial

# Função principal para executar o código
def main():
    percurso = ler_pontos_arquivo('pontos.txt')
    inicio = time.time()
    melhor_caminho, ponto_inicial = vizinho_mais_proximo(percurso)
    fim = time.time()

    return f'ponto inicial: {ponto_inicial} \ndistancia total: {melhor_caminho} \nDuração: {fim - inicio} segundos'

if __name__ == "__main__":
    print(main())
