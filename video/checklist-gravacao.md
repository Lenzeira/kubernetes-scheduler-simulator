# Checklist da gravação

Antes de gravar o vídeo, conferir:

## GitHub

- Repositório público
- README atualizado
- Pastas principais visíveis
- Código enviado para a branch main

## Execução

- Ambiente virtual ativado
- Dependências instaladas
- Projeto rodando com python3 main.py
- Script bash scripts/run.sh funcionando
- Relatório sendo gerado

## Testes

- Testes passando com bash scripts/test.sh
- Resultado esperado: 6 passed

## Pontos obrigatórios para mostrar no vídeo

- Nodo Master
- Nodos Workers
- PODs criados
- Métricas usadas
- Algoritmo proposto
- Distribuição dos PODs
- PODs pendentes
- Uso de recursos por Worker
- Estatísticas
- Comparação com o escalonador padrão
- Estrutura no GitHub

## Comandos úteis

source .venv/bin/activate
python3 main.py
bash scripts/run.sh
bash scripts/test.sh
bash scripts/show-report.sh
git status
