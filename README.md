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
