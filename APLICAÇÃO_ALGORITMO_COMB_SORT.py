"""
Trabalho - Algoritmos de Ordenação (COMB-SORT).

Emanoel do Prado | Roberto Otto

Objetivo: Implementar o Comb Sort (ordenação em pente) e medir seu tempo de execução em
vetores de 100 a 1.000.000 de elementos, em cinco cenários de organização
inicial. Os testes que passam de duas horas são interrompidos e registrados
como "Tempo de execução superior a duas horas".
"""

import multiprocessing as mp
import random
import time

tamanhos = [100, 1000, 10000, 100000, 1000000]
limite_segundos = 7200  # Duas Horas
fator_reducao = 1.3  # Fator de decréscimo padrão do Comb Sort
texto_timeout = "Tempo de execução superior a duas horas"

########### Função de Geração dos Cenários Estabelecidos ###########
"""
    Aqui geramos os cinco cenários de teste a partir dos mesmos valores numéricos.
    
    O sorted() é usado apenas para montar os cenários; o algoritmo do Comb Sort não utiliza-se do mesmo.

    Cria-se um vetor aleatório de inteiros entre 1 e 10.000 (com repetições) e
    deriva dele os demais cenários, alterando apenas a organização.

    Parâmetros:
        tamanho (int): quantidade de elementos de cada vetor.

    Retorna:
        dict: nome do cenário -> lista. Chaves: "Aleatório", "Crescente",
        "Decrescente", "Quase (Maior no Início)" e "Quase (Menor no Fim)".
    """


def gerar_cenarios(tamanho):
    # Gera o vetor base, permite números repetidos.
    aleatorio = [random.randint(1, 10000) for _ in range(tamanho)]
    crescente = sorted(aleatorio)
    decrescente = sorted(aleatorio, reverse=True)

    quase_maior_inicio = sorted(aleatorio)
    maior = quase_maior_inicio.pop()  # Remove o maior elemento do final
    quase_maior_inicio.insert(0, maior)  # Insere o maior na primeira posição

    quase_menor_fim = sorted(aleatorio)
    menor = quase_menor_fim.pop(0)
    quase_menor_fim.append(menor)

    return {
        "Aleatório": aleatorio,
        "Crescente": crescente,
        "Decrescente": decrescente,
        "Quase (Maior no Início)": quase_maior_inicio,
        "Quase (Menor no Fim)": quase_menor_fim,
    }

########### Função do Algoritmo de Ordenação (Comb Sort / Ordenação em Pente) ###########


def algoritmo_pente(vetor):
    """
    Esta função parte da aplicação de ordenação de um vetor em ordem crescente usando Comb Sort (ordenação em pente).

    Compara elementos separados por um espaçamento que começa no tamanho do
    vetor e é dividido por 1,3 a cada passada. Quando chega a 1, o algoritmo
    se comporta como um Bubble Sort e repete até não haver mais trocas.
    A ordenação é feita no próprio vetor (in-place).

    Parâmetros:
        vetor (list): lista de números a ser ordenada (modificada no lugar).

    Retorna:
        list: o mesmo vetor, já ordenado.
    """
    tamanho = len(vetor)
    espacamento = tamanho
    ordenado = False

    while not ordenado:
        espacamento = int(espacamento / fator_reducao)

        if espacamento in (9, 10):
            # Aplicação do CombSort11, padronizando os espacamentos e evitando erros.
            espacamento = 11

        if espacamento <= 1:
            espacamento = 1
            ordenado = True  # A partir daqui, ele se comporta igual ao Bubble Sort

        i = 0
        while i + espacamento < tamanho:
            # Compara dois elementos, o elemento 1 deve ser menor que o elemento 2
            if vetor[i] > vetor[i + espacamento]:
                # Troca ambos os elementos de ordem
                vetor[i], vetor[i + espacamento] = vetor[i + espacamento], vetor[i]
                ordenado = False
            i += 1

    return vetor


def esta_ordenado(vetor):
    """
    Verificamos se o vetor está em ordem crescente (não decrescente).

    Parâmetros:
        vetor (list): lista de números a verificar.

    Retorna:
        bool: True se cada elemento é menor ou igual ao seguinte.
    """
    return all(vetor[i] <= vetor[i + 1] for i in range(len(vetor) - 1))  # Percorre o vetor e verifica se cada elemento é menor ou igual ao próximo

########### Execução em processo separado (para interromper após duas horas de execução) ###########


def _executar(vetor, fila):
    """
    Executa de fato o Comb Sort e medimos o tempo, dentro de um processo separado.

    O tempo é medido com time.perf_counter() apenas durante a ordenação.
    Ao final, envia (tempo, ordenado_corretamente) pela fila.

    Parâmetros:
        vetor (list): cópia do vetor a ser ordenado.
        fila (multiprocessing.Queue): fila usada para devolver o resultado
            ao processo principal.
    """
    inicio = time.perf_counter()  # Registra o tempo inicial exato
    algoritmo_pente(vetor)
    tempo = time.perf_counter() - inicio
    # Coloca os resultados para validação
    fila.put((tempo, esta_ordenado(vetor)))


def medir(vetor, limite):
    """
    Aqui medimos o tempo do Comb Sort em um processo separado, com limite de tempo.

    Usa um processo (e não uma thread) porque ele pode ser encerrado à força
    com terminate() caso ultrapasse o limite de duas horas.

    Parâmetros:
        vetor (list): vetor a ser ordenado (uma cópia é enviada ao processo).
        limite (int | float): tempo máximo de execução, em segundos.

    Retorna:
        tuple: (tempo_em_segundos, ordenado_corretamente), ou (None, False)
        se o limite foi ultrapassado.
    """
    fila = mp.Queue()  # Cria a fila de processos
    processo = mp.Process(target=_executar, args=(list(vetor), fila))
    processo.start()
    processo.join(timeout=limite)

    if processo.is_alive():  # Se o processo for maior que o limite
        processo.terminate()
        processo.join()
        return None, False

    # Caso não seja maior que o limite, devolve o tempo e o resultado da fila
    return fila.get(timeout=10)

########### Impressão das Tabelas ###########


def imprimir_tabela(resultados, nomes_cenarios):
    """
    Imprime no terminal a tabela de tempos, com tamanhos nas linhas e
    cenários nas colunas.

    Parâmetros:
        resultados (dict): tamanho -> {nome do cenário -> texto do tempo}.
        nomes_cenarios (list[str]): nomes dos cenários, na ordem das colunas.
    """
    larguras = [max(len(n), 12) for n in nomes_cenarios]
    cabecalho = "Tamanho".ljust(10) + " | " + " | ".join(
        # Criação com alinhamento a esquerda dentro do width.
        n.ljust(w) for n, w in zip(nomes_cenarios, larguras)
    )
    print(cabecalho)
    print("-" * len(cabecalho))

    for tamanho in tamanhos:
        celulas = []
        for nome, w in zip(nomes_cenarios, larguras):
            valor = resultados[tamanho][nome]
            celulas.append(valor.ljust(w))
        print(f"{tamanho:<10} | " + " | ".join(celulas))


########### Definição do main ###########
def main():
    """
    Programa principal: executa a demonstração e a bateria de testes.

    Mostra a demonstração dos cenários com 10 elementos e, para cada tamanho
    de vetor, gera os cinco cenários e mede o tempo do Comb Sort em cada um
    (com limite de duas horas). No final, imprime a tabela de tempos.
    """
    print("=" * 30)
    print("Demonstração da Funcionalidade dos Cenários (com 10 Elementos)")
    print("=" * 30)
    # Aqui, geramos 10 elementos e o imprimimos no terminal para comprovação que os vetores estão sendo gerados corretamente
    cenarios_exemplo = gerar_cenarios(10)
    for nome_cenario, dados in cenarios_exemplo.items():
        print(f"{nome_cenario}: {dados}")
    print("=" * 30)

    ########### Programa Principal ###########
    resultados = {}
    nomes_cenarios = []

    for tamanho in tamanhos:  # Percorre o tamanho exigido (100 a 1.000.000)
        cenarios = gerar_cenarios(tamanho)
        nomes_cenarios = list(cenarios.keys())
        resultados[tamanho] = {}

        print("=" * 30)
        print(f"Testando para o vetor de {tamanho} elementos.")
        print("=" * 30)

        for nome_cenario, dados in cenarios.items():
            # Para cada cenário, chamamos a função medir para aplicarmos o limite de tempo
            tempo, ok = medir(dados, limite_segundos)

            if tempo is None:
                resultados[tamanho][nome_cenario] = texto_timeout
                # Aqui só entra se o tempo ultrapassou as duas horas
                print(f"[{nome_cenario}] -> {texto_timeout}.")

            else:
                resultados[tamanho][nome_cenario] = f"{tempo:.4f} s"
                # Aqui só entra se o vetor não ficou ordenado devido a algum erro no algoritmo
                status = "OK" if ok else "Erro; vetor não ficou ordenado!"
                print(f"[{nome_cenario}] -> {tempo:.4f} segundos ({status})")

    print("\n" + "=" * 30)
    print("TABELA FINAL DE TEMPOS")
    print("=" * 30)

    # Exibição final para termos um resumo completo no terminal
    imprimir_tabela(resultados, nomes_cenarios)
    print("=" * 30)


if __name__ == "__main__":  # Chama o programa principal, o separamos em if para podermos ter um docstring no def __main__
    main()
