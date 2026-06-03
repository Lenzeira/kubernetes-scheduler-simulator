# Roteiro do vídeo de apresentação

Tempo estimado: 10 minutos.

## 1. Apresentação do objetivo

Explicar que o projeto simula um escalonador de PODs inspirado no Kubernetes.

Apresentar rapidamente a ideia de Master, Workers e PODs.

## 2. Técnica escolhida

Explicar que a implementação foi feita em Python, usando simulação single-thread orientada a objetos.

Justificar que essa escolha facilita a visualização da lógica de escalonamento.

## 3. Estrutura do projeto

Mostrar no GitHub as principais pastas:

- config
- src
- reports
- scripts
- tests
- docs

## 4. Explicação das estruturas

Explicar os principais arquivos:

- pod.py
- worker.py
- master.py
- scheduler.py
- metrics.py
- report.py

## 5. Métricas utilizadas

Explicar as quatro métricas do escalonador proposto:

- CPU
- memória
- disco
- latência

Comparar com o escalonador padrão simulado, que usa apenas CPU e memória.

## 6. Execução do projeto

Rodar:

```bash
python3 main.py
