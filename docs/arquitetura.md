# Arquitetura da simulação

Este projeto simula o funcionamento básico de um escalonador de PODs inspirado no Kubernetes.

A estrutura principal é formada por três elementos:

- Master
- Workers
- PODs

O Master recebe os PODs, organiza a ordem de processamento por prioridade e chama o escalonador responsável por decidir em qual Worker cada POD será alocado.

## Fluxo geral

```text
config/pods.json       config/workers.json
       |                       |
       +----------+------------+
                  |
               main.py
                  |
                Master
                  |
        +---------+----------+
        |                    |
Escalonador proposto   Escalonador padrão
        |                    |
        +---------+----------+
                  |
               Workers
                  |
      PODs alocados e PODs pendentes
                  |
       Terminal + reports/resultados.txt
