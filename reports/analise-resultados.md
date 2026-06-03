# Análise dos resultados

A simulação processa 15 PODs em 3 Workers.

Foram comparadas duas estratégias de escalonamento:

- BalancedResourceScheduler
- KubernetesDefaultScheduler

## Escalonador proposto

O escalonador proposto alocou 10 PODs e deixou 5 pendentes.

Mesmo alocando menos PODs que o escalonador padrão simulado, ele não gerou violações de disco ou latência.

Isso mostra que o algoritmo foi mais cuidadoso na escolha dos Workers.

## Escalonador padrão simulado

O escalonador padrão simulado alocou 11 PODs e deixou 4 pendentes.

Porém, como considera apenas CPU e memória, ele gerou violações em métricas extras.

As violações ocorreram principalmente por uso de disco acima da capacidade do Worker e por latência acima do limite aceito pelo POD.

## Comparação

| Escalonador | PODs alocados | PODs pendentes | Violações |
|---|---:|---:|---:|
| BalancedResourceScheduler | 10 | 5 | 0 |
| KubernetesDefaultScheduler | 11 | 4 | 5 |

## Leitura final

O resultado reforça a importância de usar mais métricas no processo de escalonamento.

A solução proposta não busca apenas ocupar os Workers, mas fazer isso respeitando limites importantes dos recursos computacionais.
