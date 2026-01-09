# Makefile for Sports Betting System

.PHONY: help install test run dev paper-trading setup clean format lint

help:
	@echo "Sports Betting System - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup and Installation:"
	@echo "  make setup          - Complete project setup (venv + dependencies)"
	@echo "  make install        - Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Run in development mode (paper trading)"
	@echo "  make run            - Run main application"
	@echo "  make paper-trading  - Run with paper trading enabled"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         - Format code with black"
	@echo "  make lint           - Run linters (pylint, ruff)"
	@echo "  make test           - Run unit tests"
	@echo ""
	@echo "Database:"
	@echo "  make db-init        - Initialize PostgreSQL database"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Remove cache and compiled files"
	@echo "  make requirements   - Generate requirements.txt"
	@echo ""

setup:
	@echo "Setting up Sports Betting System..."
	python -m venv venv
	. venv/Scripts/activate && pip install --upgrade pip
	. venv/Scripts/activate && pip install -r requirements.txt
	@echo "✓ Setup complete! Run 'make dev' to start"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v --cov=src

run:
	python main.py

dev:
	@echo "Running in DEVELOPMENT mode (Paper Trading)..."
	ENVIRONMENT=development PAPER_TRADING=True python main.py

paper-trading:
	@echo "Running PAPER TRADING mode (simulated bets)..."
	PAPER_TRADING=True LIVE_TRADING=False python main.py

lint:
	pylint src/
	ruff check src/ tests/

format:
	black src/ tests/ main.py config.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage coverage_html_report/

db-init:
	@echo "Initializing PostgreSQL database..."
	psql -U postgres -f database/schema.sql
	@echo "✓ Database schema created"

requirements:
	pip freeze > requirements.txt

.DEFAULT_GOAL := help
