#!/bin/bash

# Base directory
mkdir -p form-app

# Subdirectories
mkdir -p form-app/src
mkdir -p form-app/config
mkdir -p form-app/tests
mkdir -p form-app/docs
mkdir -p form-app/scripts

# Creating initial files
touch form-app/src/main.py
touch form-app/src/app.py
touch form-app/config/eqinspect.yml
touch form-app/config/eqcheckin.yml
touch form-app/tests/test_app.py
touch form-app/docs/README.md

# .gitignore with some defaults
cat <<EOT > form-app/.gitignore
# Python cache and compiled files
__pycache__/
*.py[cod]

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/
EOT

echo "Project structure and basic files created."
