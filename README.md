# Kubernetes Scheduler Simulator

Simulador de escalonamento de PODs inspirado no funcionamento do Kubernetes, desenvolvido em Python.

O projeto implementa:

- Nodo Master
- Nodos Workers
- PODs com diferentes requisitos computacionais
- Algoritmo de escalonamento balanceado
- Comparação com algoritmo First Fit
- Monitoramento de recursos
- Estatísticas de alocação

---

# Técnica Escolhida

A técnica escolhida para o desenvolvimento foi uma simulação single-thread orientada a objetos.

A escolha por single-thread foi feita para manter o funcionamento do escalonador mais claro, determinístico e fácil de analisar.

Como o foco principal do trabalho está na lógica de escalonamento, na distribuição dos PODs e no gerenciamento de recursos dos Workers, a abordagem single-thread permite visualizar melhor cada decisão tomada pelo Master e pelos algoritmos implementados.

O projeto não utiliza multithreading ou produtor/consumidor porque o objetivo principal não é simular concorrência entre processos, mas demonstrar estratégias de escalonamento inspiradas no Kubernetes.

---

# Estrutura do Projeto

```text
kubernetes-scheduler-simulator/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── src/
    ├── pod.py
    ├── worker.py
    ├── master.py
    ├── scheduler.py
    └── metrics.py
