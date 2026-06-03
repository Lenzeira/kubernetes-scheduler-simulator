# Kubernetes Scheduler Simulator

Este projeto é uma simulação em Python de um escalonador de PODs inspirado no funcionamento do Kubernetes.

A ideia do trabalho é representar um ambiente com um nodo Master, alguns Workers e um conjunto de PODs com diferentes necessidades computacionais. A partir disso, o sistema decide onde cada POD deve ser alocado, considerando os recursos disponíveis em cada Worker.

A implementação foi feita em simulação, rodando localmente pelo terminal Linux. Essa escolha permite focar na lógica do escalonador, na comparação entre estratégias de alocação e na visualização dos recursos ocupados e disponíveis.

---

## Visão geral do projeto

A simulação trabalha com:

| Elemento | Quantidade |
|---|---:|
| Master | 1 |
| Workers | 3 |
| PODs | 15 |
| Métricas de alocação | 4 |
| Algoritmos comparados | 2 |
| Relatório automático | Sim |
| Testes automatizados | Sim |

O projeto compara dois comportamentos:

| Escalonador | Métricas consideradas |
|---|---|
| `BalancedResourceScheduler` | CPU, memória, disco e latência |
| `KubernetesDefaultScheduler` | CPU e memória |

O escalonador proposto considera mais métricas do que a versão usada como referência do Kubernetes. Isso permite observar situações em que um Worker parece adequado olhando apenas para CPU e memória, mas não seria uma boa escolha quando disco e latência também são considerados.

---

## Técnica escolhida

A técnica escolhida foi uma simulação **single-thread** com programação orientada a objetos.

Essa escolha foi feita para deixar a execução mais clara e fácil de acompanhar. Como o foco do trabalho está no processo de escalonamento, a abordagem single-thread permite visualizar melhor a ordem das decisões, a escolha dos Workers e os motivos pelos quais alguns PODs são alocados ou ficam pendentes.

O projeto não usa multithreading nem produtor-consumidor porque a proposta principal não é simular concorrência entre processos. O foco está na lógica de alocação dos PODs e na comparação entre os algoritmos.

---

## Como a simulação funciona

A simulação começa a partir de dois arquivos de configuração:

| Arquivo | Função |
|---|---|
| `config/pods.json` | Define os PODs que serão processados |
| `config/workers.json` | Define os Workers disponíveis e suas capacidades |

O fluxo geral é este:

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
```

O `main.py` carrega os dados, cria os objetos da simulação, executa os dois escalonadores e mostra os resultados no terminal. Ao final, também é gerado um relatório em `reports/resultados.txt`.

---

## Métricas de alocação

O escalonador proposto considera quatro métricas:

| Métrica | O que representa |
|---|---|
| CPU | Capacidade de processamento disponível no Worker |
| Memória | Quantidade de memória disponível |
| Disco | Espaço de armazenamento disponível |
| Latência | Tempo de resposta do Worker em relação ao limite aceito pelo POD |

A simulação do escalonador padrão considera apenas:

| Métrica | O que representa |
|---|---|
| CPU | Capacidade de processamento |
| Memória | Quantidade de memória disponível |

Essa diferença é importante porque mostra que uma alocação pode parecer válida usando apenas CPU e memória, mas ainda assim causar problemas quando outras métricas entram na análise.

---

## Estruturas principais

### Master

O Master é o nodo central da simulação.

Ele recebe a lista de PODs, organiza a ordem de processamento por prioridade e chama o escalonador para decidir onde cada POD será alocado.

### Workers

Os Workers representam os nodos disponíveis para receber os PODs.

Cada Worker possui:

```text
CPU total
memória total
disco total
latência
CPU usada
memória usada
disco usado
PODs alocados
violações registradas
```

### PODs

Cada POD representa uma aplicação ou tarefa que precisa ser alocada em algum Worker.

Cada POD possui:

```text
nome
CPU necessária
memória necessária
disco necessário
latência máxima aceita
perfil de carga
prioridade
Worker alocado
```

---

## Perfis de POD

Os PODs possuem perfis diferentes para representar tipos variados de carga.

| Perfil | Característica |
|---|---|
| `light` | Baixo consumo geral |
| `balanced` | Uso equilibrado dos recursos |
| `cpu` | Maior dependência de processamento |
| `memory` | Maior dependência de memória |
| `storage` | Maior dependência de disco |
| `latency` | Maior sensibilidade à latência |

Esses perfis influenciam o cálculo do escalonador proposto. Por exemplo, um POD com perfil `storage` dá mais importância ao espaço em disco, enquanto um POD com perfil `latency` prioriza Workers com menor latência.

---

## Algoritmos implementados

### BalancedResourceScheduler

Este é o escalonador proposto no trabalho.

Ele avalia os Workers disponíveis considerando CPU, memória, disco, latência e perfil do POD. A decisão não é feita apenas escolhendo o primeiro Worker livre. O algoritmo calcula uma pontuação para cada Worker viável e seleciona aquele que oferece a melhor condição para o POD.

Fluxo simplificado:

```text
1. Receber POD
2. Verificar Workers disponíveis
3. Validar CPU, memória, disco e latência
4. Calcular pontuação dos Workers viáveis
5. Escolher o Worker com melhor pontuação
6. Alocar o POD ou registrar como pendente
```

A pontuação segue esta ideia:

```text
score =
    peso_cpu      * cpu_livre
  + peso_memoria  * memoria_livre
  + peso_disco    * disco_livre
  + peso_latencia * score_latencia
```

A latência é tratada de forma inversa. Quanto menor a latência do Worker em relação ao limite aceito pelo POD, melhor a pontuação.

---

### KubernetesDefaultScheduler

Este escalonador representa uma versão simplificada do comportamento padrão do Kubernetes dentro da simulação.

Ele considera apenas CPU e memória durante a decisão de alocação. As métricas de disco e latência são ignoradas.

Essa comparação ajuda a mostrar que uma decisão baseada somente em CPU e memória pode alocar mais PODs, mas também pode gerar violações em métricas importantes para o funcionamento da aplicação.

---

## Resultado da execução

Na configuração atual, o projeto processa 15 PODs em 3 Workers.

| Escalonador | PODs alocados | PODs pendentes | Taxa de alocação | Violações |
|---|---:|---:|---:|---:|
| Escalonador proposto | 10 | 5 | 66.67% | 0 |
| Escalonador padrão do Kubernetes | 11 | 4 | 73.33% | 5 |

O escalonador padrão alocou mais PODs, mas gerou violações de disco e latência.

O escalonador proposto foi mais restritivo, mas respeitou todas as métricas adicionais. Isso mostra que a melhor decisão de escalonamento não é necessariamente aquela que aloca mais PODs, mas aquela que respeita melhor os limites dos Workers e os requisitos das aplicações.

---

## Exemplo de saída

Trecho resumido da execução:

```text
SIMULAÇÃO COM ESCALONADOR PROPOSTO
Total de PODs processados: 15
PODs alocados: 10
PODs pendentes: 5
Taxa de alocação: 66.67%
Violações de métricas extras: nenhuma

SIMULAÇÃO COM ESCALONADOR PADRÃO DO KUBERNETES
Total de PODs processados: 15
PODs alocados: 11
PODs pendentes: 4
Taxa de alocação: 73.33%
Violações de métricas extras: 5
```

---

## Estrutura do projeto

```text
kubernetes-scheduler-simulator/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
│   ├── pods.json
│   └── workers.json
│
├── reports/
│   └── resultados.txt
│
├── scripts/
│   └── run.sh
│
├── src/
│   ├── __init__.py
│   ├── master.py
│   ├── metrics.py
│   ├── pod.py
│   ├── report.py
│   ├── scheduler.py
│   └── worker.py
│
└── tests/
    └── test_scheduler.py
```

---

## Principais arquivos

| Arquivo | Função |
|---|---|
| `main.py` | Executa a simulação, compara os escalonadores e gera o relatório |
| `config/pods.json` | Define os PODs, seus requisitos, perfis e prioridades |
| `config/workers.json` | Define os Workers e suas capacidades |
| `src/pod.py` | Implementa a estrutura dos PODs |
| `src/worker.py` | Implementa os Workers e controla seus recursos |
| `src/master.py` | Implementa o nodo Master |
| `src/scheduler.py` | Contém os algoritmos de escalonamento |
| `src/metrics.py` | Mostra métricas e status no terminal |
| `src/report.py` | Gera o relatório final |
| `reports/resultados.txt` | Armazena o resultado da última execução |
| `scripts/run.sh` | Script simples para rodar o projeto pelo terminal |
| `tests/test_scheduler.py` | Testes automatizados |

---

## Pré-requisitos

Para executar o projeto, é necessário ter:

```text
Python 3
Git
Terminal Linux
```

Para rodar os testes, também é necessário instalar o Pytest.

---

## Como executar

Clone o repositório:

```bash
git clone https://github.com/Lenzeira/kubernetes-scheduler-simulator.git
```

Entre na pasta do projeto:

```bash
cd kubernetes-scheduler-simulator
```

Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a simulação:

```bash
python3 main.py
```

Também é possível executar pelo script:

```bash
bash scripts/run.sh
```

---

## Testes

Para executar os testes automatizados:

```bash
PYTHONPATH=. pytest
```

Resultado esperado:

```text
6 passed
```

Os testes cobrem:

| Teste | O que verifica |
|---|---|
| Alocação com todas as métricas | Confirma que um POD válido pode ser alocado |
| Disco insuficiente | Confirma rejeição quando não há espaço em disco |
| Latência alta | Confirma rejeição quando a latência passa do limite |
| Escalonador proposto | Confirma seleção de Worker viável |
| Escalonador padrão | Confirma que disco e latência são ignorados |
| POD pendente | Confirma registro de PODs não alocados |

---

## Relatório

A cada execução, o sistema gera automaticamente:

```text
reports/resultados.txt
```

O relatório apresenta:

```text
total de PODs processados
PODs alocados
PODs pendentes
taxa de alocação
uso de CPU, memória e disco por Worker
latência de cada Worker
PODs alocados em cada Worker
violações de métricas extras
```

Esse arquivo ajuda na análise dos resultados e também serve como apoio para a apresentação do trabalho.

---

## Relação com os critérios do trabalho

| Critério | Atendimento no projeto |
|---|---|
| Estrutura do Master | Classe `Master` em `src/master.py` |
| Workers e capacidades | Classe `Worker` e arquivo `config/workers.json` |
| Mais de uma dezena de PODs | 15 PODs definidos em `config/pods.json` |
| Métricas de alocação | CPU, memória, disco e latência |
| Algoritmo de escalonamento | `BalancedResourceScheduler` |
| Distribuição dos PODs | Exibida no terminal e no relatório |
| Monitoramento | Uso de recursos por Worker |
| Estatísticas | Taxa de alocação, pendências e violações |
| Comparação com Kubernetes | `KubernetesDefaultScheduler` |
| Reprodutibilidade | README, script, testes e GitHub |

---

## Sobre o script Shell

O arquivo `scripts/run.sh` é apenas um atalho para executar o projeto pelo terminal Linux.

Por esse motivo, o GitHub pode mostrar uma pequena porcentagem da linguagem `Shell` no repositório. A maior parte do projeto continua sendo Python.

---

## Observações finais

Esta implementação não executa PODs reais em um cluster Kubernetes. Ela reproduz, em simulação, os elementos centrais pedidos no trabalho: Master, Workers, PODs, métricas de alocação, algoritmo de escalonamento, monitoramento, estatísticas e comparação com uma estratégia baseada no escalonador padrão.

A escolha pela simulação permitiu concentrar a implementação na lógica do escalonador e na análise das decisões tomadas durante a alocação dos PODs.
