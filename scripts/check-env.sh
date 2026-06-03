#!/bin/bash

echo "Verificando ambiente do projeto..."
echo ""

echo "Python:"
python3 --version

echo ""
echo "Pip:"
pip --version

echo ""
echo "Pytest:"
pytest --version

echo ""
echo "Git:"
git --version

echo ""
echo "Ambiente verificado."
