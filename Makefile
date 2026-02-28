.PHONY: help setup test lint run clean

PYTHON := python
PIP    := pip

help:  ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup:  ## Crea el entorno virtual e instala dependencias
	$(PYTHON) -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -e .
	cp -n .env.example .env || true
	@echo "✅  Entorno listo. Actívalo con: source venv/bin/activate"

test:  ## Ejecuta los tests con pytest
	$(PYTHON) -m pytest tests/ -v

test-cov:  ## Tests con informe de cobertura
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing

lint:  ## Comprueba el estilo del código con ruff
	$(PYTHON) -m ruff check src/ tests/

run:  ## Ejecuta el pipeline principal
	$(PYTHON) -m src.main

notebook:  ## Lanza JupyterLab
	jupyter lab notebooks/

clean:  ## Elimina cachés y artefactos de build
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info"   -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "🧹  Limpieza completada"
