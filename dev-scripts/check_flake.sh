#!/bin/bash
echo "Kontrola flake8..."

flake8 main.py --max-line-length 120
