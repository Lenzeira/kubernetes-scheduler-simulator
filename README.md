# Kubernetes Scheduler Simulator

Simulador de escalonamento de PODs inspirado no funcionamento do Kubernetes, desenvolvido em Python para a disciplina de Laboratório de Sistemas Operacionais.

O projeto implementa uma solução single-thread orientada a objetos, com um nodo Master, múltiplos nodos Workers e PODs com diferentes requisitos computacionais.

A proposta é comparar um escalonador customizado, que considera métricas adicionais de alocação, com uma simulação do escalonador padrão do Kubernetes, que considera apenas CPU e memória.

---

## Técnica Escolhida

A técnica escolhida para o desenvolvimento foi uma simulação single-thread orientada a objetos.

Essa escolha foi feita para manter o funcionamento do escalonador mais claro, determinístico e fácil de analisar. Como o foco principal do trabalho está na lógica de escalonamento, na distribuição dos PODs e no gerenciamento dos recursos dos Workers, a abordagem single-thread permite acompanhar cada decisão tomada pelo Master e pelos algoritmos implementados.

O projeto não utiliza multithreading ou paradigma produtor-consumidor porque o objetivo principal não é simular concorrência entre processos, mas demonstrar estratégias de escalonamento de PODs em um ambiente inspirado no Kubernetes.

---

## Objetivo do Projeto

O objetivo do projeto é simular o processo de alocação de PODs em nodos Workers, utilizando um nodo Master responsável por coordenar o escalonamento.

A solução considera mais métricas do que o escalonador padrão do Kubernetes, permitindo observar como diferentes critérios podem afetar a distribuição dos PODs e o uso dos recursos computacionais.

---

## Métricas de Alocação

O escalonador proposto considera quatro métricas:

- CPU
- Memória
- Disco
- Latência

A comparação é feita com uma simulação do escalonador padrão do Kubernetes, que considera apenas:

- CPU
- Memória

Com isso, o projeto mostra que um escalonador que ignora métricas extras pode até alocar mais PODs, mas também pode gerar violações, como uso de disco acima da capacidade do Worker ou latência acima do limite aceito pelo POD.

---

## Estrutura do Projeto

```text
kubernetes-scheduler-simulator/

main.py
README.md
requirements.txt
.gitignore

config/
workers.json
pods.json

reports/
resultados.txt

scripts/
run.sh

src/
__init__.py
pod.py
worker.py
master.py
scheduler.py
metrics.py
report.py

tests/
test_scheduler.py
```

---

## Tecnologias Utilizadas

- Python 3
- Shell Script
- Git
- Linux Terminal
- Pytest

---

## Componentes Implementados

### Pod

Representa uma aplicação ou tarefa que precisa ser escalonada.

Cada POD possui:

- Nome
- CPU necessária
- Memória necessária
- Disco necessário
- Latência máxima aceita
- Perfil de carga
- Prioridade

### Worker

Representa um nodo computacional disponível para receber PODs.

Cada Worker possui:

- CPU total
- Memória total
- Disco total
- Latência
- Recursos utilizados
- Lista de PODs alocados

### Master

Representa o nodo central do sistema.

O Master é responsável por:

- Receber a lista de PODs
- Ordenar os PODs por prioridade
- Acionar o algoritmo de escalonamento
- Registrar PODs alocados
- Registrar PODs pendentes

---

## Algoritmos de Escalonamento

### BalancedResourceScheduler

É o escalonador proposto no projeto.

Ele avalia os Workers disponíveis considerando:

- CPU livre
- Memória livre
- Disco livre
- Latência do Worker
- Perfil do POD
- Prioridade do POD

O objetivo do algoritmo não é apenas alocar o maior número possível de PODs, mas realizar uma alocação mais criteriosa, respeitando métricas extras que impactam diretamente o funcionamento das aplicações.

### KubernetesDefaultScheduler

Representa uma simulação simplificada do escalonador padrão do Kubernetes.

Neste projeto, ele considera apenas:

- CPU
- Memória

Essa comparação permite mostrar o impacto de ignorar outras métricas, como disco e latência.

---

## Configuração da Simulação

Os Workers são configurados no arquivo:

```text
config/workers.json
```

Os PODs são configurados no arquivo:

```text
config/pods.json
```

A simulação atual possui:

- 3 Workers
- 15 PODs
- 4 métricas de alocação
- 2 algoritmos comparados

---

## Como Executar

### Criar ambiente virtual

```bash
python3 -m venv .venv
```

### Ativar ambiente virtual

```bash
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar pelo Python

```bash
python3 main.py
```

### Executar pelo script

```bash
bash scripts/run.sh
```

---

## Relatório Gerado

Após a execução, o sistema gera automaticamente o relatório:

```text
reports/resultados.txt
```

Esse relatório contém:

- Total de PODs processados
- PODs alocados
- PODs pendentes
- Taxa de alocação
- Uso de CPU, memória e disco por Worker
- Latência dos Workers
- Lista de PODs alocados em cada Worker
- Violações de métricas extras

---

## Resultados da Simulação

### Escalonador Proposto

- Total de PODs: 15
- PODs alocados: 10
- PODs pendentes: 5
- Taxa de alocação: 66.67%
- Violações de métricas extras: nenhuma

### Escalonador Padrão do Kubernetes

- Total de PODs: 15
- PODs alocados: 11
- PODs pendentes: 4
- Taxa de alocação: 73.33%
- Violações de métricas extras: 5

Apesar de o escalonador padrão alocar mais PODs, ele gera violações de disco e latência. Já o escalonador proposto é mais restritivo, mas respeita as métricas adicionais definidas no trabalho.

Essa diferença é importante porque mostra que a melhor solução nem sempre é aquela que aloca mais PODs, mas aquela que respeita melhor os limites dos Workers e os requisitos das aplicações.

---

## Execução dos Testes

Para executar os testes automatizados:

```bash
PYTHONPATH=. pytest
```

Os testes verificam:

- Alocação de PODs considerando todas as métricas
- Rejeição de PODs por disco insuficiente
- Rejeição de PODs por latência acima do limite
- Seleção correta de Worker pelo escalonador proposto
- Comportamento do escalonador padrão ignorando disco e latência
- Registro de PODs pendentes pelo Master

---

## Comparação Técnica com o Kubernetes

O escalonador padrão do Kubernetes utiliza CPU e memória como critérios principais de decisão.

Neste projeto, a solução proposta amplia essa lógica ao considerar também disco e latência. Dessa forma, o escalonador customizado consegue evitar alocações que, mesmo possíveis do ponto de vista de CPU e memória, seriam problemáticas para outras métricas importantes do sistema.

Na simulação executada, o escalonador padrão alocou mais PODs, porém gerou violações de disco e latência. O escalonador proposto alocou menos PODs, mas manteve a integridade das métricas adicionais.

---

## Objetivo Acadêmico

Este projeto foi desenvolvido para fins acadêmicos, com foco nos conceitos de:

- Sistemas Operacionais
- Escalonamento
- Gerenciamento de recursos
- Shell Script
- Simulação de ambiente Kubernetes
- Comparação entre algoritmos
- Organização e reprodutibilidade em GitHub
