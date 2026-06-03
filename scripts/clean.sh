#!/bin/bash

echo "Removendo arquivos temporários do Python..."
echo ""

find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "Limpeza concluída."
