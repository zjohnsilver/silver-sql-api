.PHONY: setup start dev clean test lint format help

# Default target
.DEFAULT_GOAL := help

setup: ## Setup project: create venv and install dependencies
	@echo "🔧 Setting up Silver SQL API..."
	@command -v uv >/dev/null 2>&1 || { echo "❌ uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	@echo "📦 Creating virtual environment..."
	uv venv
	@echo "📥 Installing dependencies..."
	uv pip install -e .
	@echo "📄 Copying environment file..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "✅ .env created from .env.example"; else echo "⚠️  .env already exists, skipping..."; fi
	@echo "✅ Setup complete! Run 'make start' to start the server."

start: ## Start the development server
	@echo "🚀 Starting Silver SQL API..."
	@if [ ! -d .venv ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev: start ## Alias for start

clean: ## Clean up generated files and virtual environment
	@echo "🧹 Cleaning up..."
	rm -rf .venv
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf app/**/__pycache__
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf *.egg-info
	@echo "✅ Cleanup complete!"

test: ## Run tests
	@echo "🧪 Running tests..."
	uv run pytest

lint: ## Run linter (ruff)
	@echo "🔍 Running linter..."
	uv run ruff check .

format: ## Format code with black and ruff
	@echo "✨ Formatting code..."
	uv run ruff check --fix .
	uv run black .

help: ## Show this help message
	@echo "Silver SQL API - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

