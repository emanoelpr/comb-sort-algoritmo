# Algoritmo de Ordenação — Comb Sort

**Autores:** Emanoel do Prado e Roberto Otto  
**Linguagem:** Python 3

## Sobre o projeto

Este trabalho apresentado para o modulo **ALGORITMOS E ESTRUTURA DE DADOS I** implementa o **Comb Sort**, também conhecido como *ordenação em pente*, e analisa seu tempo de execução em vetores de diferentes tamanhos e com diferentes organizações iniciais.

O objetivo é observar como a disposição dos elementos antes da ordenação influencia o desempenho do algoritmo. Para isso, o programa gera cinco cenários e executa o Comb Sort em vetores de **100, 1.000, 10.000, 100.000 e 1.000.000 de elementos**.

## Cenários analisados

Cada conjunto de cinco cenários é derivado de uma mesma lista-base de números inteiros aleatórios, entre 1 e 10.000. Assim, os cenários de um mesmo tamanho contêm os mesmos valores, mas em organizações diferentes.

| Cenário | Como o vetor é organizado |
|---|---|
| Aleatório | Valores na ordem em que foram gerados. |
| Crescente | Valores organizados do menor para o maior. |
| Decrescente | Valores organizados do maior para o menor. |
| Quase (Maior no Início) | Vetor inicialmente crescente, com o maior elemento movido para a primeira posição. |
| Quase (Menor no Fim) | Vetor inicialmente crescente, com o menor elemento movido para a última posição. |

A função `sorted()` é utilizada somente para construir os cenários crescente, decrescente e quase ordenados. **Ela não é utilizada pelo algoritmo Comb Sort que estava sendo avaliado.**

## Como o Comb Sort funciona

O Comb Sort compara elementos que estão separados por uma distância chamada **espaçamento** (*gap*). No início, esse espaçamento corresponde ao tamanho do vetor. A cada passada, ele é dividido pelo fator de redução **1,3**.

Quando o espaçamento chega a 1, o algoritmo passa a comparar elementos vizinhos, de forma semelhante ao Bubble Sort. As passadas continuam até que não haja mais trocas e o vetor esteja ordenado.

O código também aplica a otimização conhecida como **CombSort11**: quando o espaçamento calculado é 9 ou 10, ele é substituído por 11.

A ordenação é feita **no próprio vetor** (*in-place*), sem criar uma segunda lista ordenada.

## Medição do tempo

Cada execução do algoritmo acontece em um processo separado, utilizando o módulo `multiprocessing`. O tempo é medido com `time.perf_counter()`, considerando somente o período de execução da ordenação.

Foi definido um limite de **7.200 segundos (duas horas) por cenário**. Se uma execução ultrapassar esse limite, o processo é encerrado e o resultado é registrado como:

> Tempo de execução superior a duas horas

Depois de cada ordenação concluída, o programa verifica se o vetor ficou em ordem crescente. A tabela final apresenta os tamanhos dos vetores nas linhas e os cinco cenários nas colunas.

> **Atenção:** são até 25 medições (5 tamanhos × 5 cenários). Como cada medição pode durar até duas horas, uma execução completa pode levar bastante tempo. O limite de duas horas é aplicado individualmente a cada cenário, e não ao programa inteiro.

## Requisitos

- Python 3 instalado.
- Não são necessárias bibliotecas externas: o programa utiliza módulos da biblioteca padrão do Python (`multiprocessing`, `random` e `time`).

## Como executar

1. Baixe ou clone o repositório.
2. Abra o terminal na pasta em que está o arquivo Python.
3. Execute o programa:

```bash
python comb_sort.py
```

O comando acima considera que o arquivo foi renomeado para `comb_sort.py`. Caso mantenha outro nome, substitua `comb_sort.py` pelo nome correspondente.

No Windows, a execução também pode ser feita pelo PowerShell:

```powershell
python .\comb_sort.py
```

## O que aparece no terminal

Durante a execução, o programa:

1. Exibe uma demonstração dos cinco cenários com vetores de 10 elementos.
2. Gera os cinco cenários para cada tamanho definido.
3. Informa o andamento de cada medição e seu tempo, ou registra quando o limite de duas horas é ultrapassado.
4. Exibe uma tabela final com os tempos obtidos.

## Observações sobre os resultados

- Os vetores são gerados aleatoriamente a cada execução. Portanto, os valores e os tempos podem mudar entre execuções.
- Os tempos dependem também do computador e das condições em que o programa é executado.
- Os resultados representam as medições feitas por este programa, com os tamanhos, cenários e limite descritos neste README.
- O programa mede o tempo da ordenação; a geração dos cenários e a verificação final de ordenação não fazem parte do intervalo cronometrado.

## Estrutura principal do código

| Função | Responsabilidade |
|---|---|
| `gerar_cenarios(tamanho)` | Gera a lista-base e constrói os cinco cenários. |
| `algoritmo_pente(vetor)` | Executa a ordenação Comb Sort. |
| `esta_ordenado(vetor)` | Verifica se o vetor está em ordem crescente. |
| `_executar(vetor, fila)` | Executa e cronometra o algoritmo no processo separado. |
| `medir(vetor, limite)` | Inicia o processo, aplica o limite de tempo e recebe o resultado. |
| `imprimir_tabela(resultados, nomes_cenarios)` | Exibe a tabela final de tempos. |
| `main()` | Coordena a demonstração, os cenários, as medições e a apresentação dos resultados. |

---

**Trabalho acadêmico — Algoritmos de Ordenação (COMB-SORT)**  
Emanoel do Prado | Roberto Otto
