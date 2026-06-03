# Roteiro do vídeo de apresentação

Tempo estimado: 10 minutos.

## 1. Apresentação do projeto

Apresentar o projeto como uma simulação em Python de um escalonador de PODs inspirado no Kubernetes.

Explicar rapidamente a ideia de Master, Workers e PODs.

## 2. Técnica escolhida

Explicar que a implementação foi feita em simulação single-thread orientada a objetos.

## 3. Estrutura do repositório

Mostrar as principais pastas:

- config
- src
- reports
- scripts
- tests
- docs
- video

## 4. Configuração dos Workers e PODs

Mostrar os arquivos config/workers.json e config/pods.json.

Explicar que existem 3 Workers e 15 PODs.

## 5. Algoritmos de escalonamento

Mostrar o arquivo src/scheduler.py.

Explicar os dois algoritmos:

- BalancedResourceScheduler
- KubernetesDefaultScheduler

Explicar que o escalonador proposto usa CPU, memória, disco e latência, enquanto o padrão simulado usa apenas CPU e memória.

## 6. Execução

Rodar:

bash scripts/run.sh

Mostrar os PODs alocados, os PODs pendentes e o uso dos recursos por Worker.

## 7. Relatório

Rodar:

bash scripts/show-report.sh

Explicar o resultado da comparação entre os dois escalonadores.

## 8. Testes

Rodar:

bash scripts/test.sh

Mostrar que os testes passaram.

## 9. Fechamento

Reforçar que o projeto atende aos pontos principais do trabalho: Master, Workers, mais de 10 PODs, métricas adicionais, algoritmo, monitoramento, estatísticas, comparação com Kubernetes, GitHub e documentação.
