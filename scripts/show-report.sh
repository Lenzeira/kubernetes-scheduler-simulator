#!/bin/bash

REPORT_FILE="reports/resultados.txt"

if [ -f "$REPORT_FILE" ]; then
    echo "Exibindo relatório da simulação:"
    echo ""
    cat "$REPORT_FILE"
else
    echo "Relatório não encontrado."
    echo "Execute primeiro: bash scripts/run.sh"
fi
