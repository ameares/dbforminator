#!/bin/bash

# Subdirectories
mkdir -p src
mkdir -p config
mkdir -p tests
mkdir -p docs
mkdir -p scripts

# Creating initial files
touch ./src/main.py
touch ./src/app.py
touch ./config/eqinspect.yml
touch ./config/eqcheckin.yml
touch ./tests/test_app.py
touch ./docs/README.md

# .gitignore with some defaults
cat <<EOT > ./.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
EOT

echo "Project structure and basic files created."
