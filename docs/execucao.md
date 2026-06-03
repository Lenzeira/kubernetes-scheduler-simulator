# Guia de execução

Este documento apresenta os comandos necessários para executar o projeto pelo terminal Linux.

## Entrar na pasta do projeto

cd ~/kubernetes-scheduler-simulator

## Ativar o ambiente virtual

source .venv/bin/activate

Caso o ambiente virtual não exista ou esteja quebrado:

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

## Executar a simulação

python3 main.py

Também é possível executar pelo script:

bash scripts/run.sh

## Ver o relatório

bash scripts/show-report.sh

ou:

cat reports/resultados.txt

## Rodar os testes

bash scripts/test.sh

Se o pytest não estiver instalado:

python3 -m pip install pytest

## Limpar arquivos temporários

bash scripts/clean.sh
