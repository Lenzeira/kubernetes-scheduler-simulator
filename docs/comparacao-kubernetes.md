# Comparação com o escalonador padrão do Kubernetes

O trabalho compara duas estratégias de escalonamento.

A primeira é o escalonador proposto, chamado `BalancedResourceScheduler`.

A segunda é uma simulação simplificada do escalonador padrão do Kubernetes, chamada `KubernetesDefaultScheduler`.

## Métricas utilizadas

| Escalonador | CPU | Memória | Disco | Latência |
|---|---:|---:|---:|---:|
| BalancedResourceScheduler | Sim | Sim | Sim | Sim |
| KubernetesDefaultScheduler | Sim | Sim | Não | Não |

## Interpretação

O escalonador padrão simulado considera apenas CPU e memória.

Isso faz com que ele consiga alocar mais PODs em alguns cenários, mas também pode gerar problemas quando outras métricas são observadas.

Na simulação atual, o escalonador padrão alocou mais PODs, porém gerou violações de disco e latência.

Já o escalonador proposto foi mais restritivo, mas respeitou todas as métricas adicionais.

## Resultado da execução

| Escalonador | PODs alocados | PODs pendentes | Taxa de alocação | Violações |
|---|---:|---:|---:|---:|
| BalancedResourceScheduler | 10 | 5 | 66.67% | 0 |
| KubernetesDefaultScheduler | 11 | 4 | 73.33% | 5 |

## Conclusão

A comparação mostra que alocar mais PODs não significa necessariamente fazer uma melhor distribuição.

O escalonador proposto prioriza uma alocação mais segura, respeitando CPU, memória, disco e latência.

O escalonador padrão simulado apresenta uma taxa de alocação maior, mas ignora métricas que podem afetar o funcionamento das aplicações.
