.PHONY: help test test-unit test-integration test-cov clean install run check dev

# Detectar sistema operativo
ifeq ($(OS),Windows_NT)
	PYTHON := python
	VENV_BIN := .venv/Scripts
	RM := del /Q
	RMDIR := rmdir /S /Q
else
	PYTHON := python3
	VENV_BIN := .venv/bin
	RM := rm -f
	RMDIR := rm -rf
endif

help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Instalar dependencias"
	@echo "  make check         - Verificar sistema"
	@echo "  make dev           - Iniciar en modo desarrollo"
	@echo "  make run           - Ejecutar aplicación"
	@echo "  make test          - Ejecutar todos los tests"
	@echo "  make test-unit     - Ejecutar solo tests unitarios"
	@echo "  make test-cov      - Ejecutar tests con cobertura"
	@echo "  make clean         - Limpiar archivos temporales"

install:
	$(PYTHON) -m venv .venv
	$(VENV_BIN)/pip install -r requirements.txt

check:
	$(VENV_BIN)/$(PYTHON) scripts/check_system.py

dev:
	$(VENV_BIN)/$(PYTHON) scripts/init_system.py
	$(VENV_BIN)/$(PYTHON) run.py

run:
	$(VENV_BIN)/$(PYTHON) run.py

test:
	$(VENV_BIN)/$(PYTHON) -m pytest

test-unit:
	$(VENV_BIN)/$(PYTHON) -m pytest -m unit

test-integration:
	$(VENV_BIN)/$(PYTHON) -m pytest -m integration

test-cov:
	$(VENV_BIN)/$(PYTHON) -m pytest --cov=backend --cov-report=html

clean:
ifeq ($(OS),Windows_NT)
	@echo "Limpiando archivos temporales..."
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" $(RMDIR) "%%d"
	@for /r . %%f in (*.pyc) do @if exist "%%f" $(RM) "%%f"
	@if exist .pytest_cache $(RMDIR) .pytest_cache
	@if exist htmlcov $(RMDIR) htmlcov
	@if exist .coverage $(RM) .coverage
else
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	$(RMDIR) .pytest_cache 2>/dev/null || true
	$(RMDIR) htmlcov 2>/dev/null || true
	$(RM) .coverage 2>/dev/null || true
endif
	@echo "Limpieza completada"
