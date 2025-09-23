# PyData MCP Workshop Makefile
# Commands for running workshop exercises and managing the development environment

.PHONY: help setup test clean workshop-* solution-* server-* dev lint format check-env

help:
	@echo "PyData MCP Workshop Commands"
	@echo "============================"
	@echo ""
	@echo "Setup:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(setup|clean|check-env):' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Workshop Exercises:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^workshop-' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[32m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Solutions:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^solution-' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[33m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Development:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(dev|test|lint|format):' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[34m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and sync environment
	@echo "🔧 Setting up workshop environment..."
	uv sync
	@echo "✅ Environment ready!"

check-env: ## Validate environment setup (API keys, dependencies)
	@echo "🔍 Checking environment..."
	uv run python -c "import solution.clients.config; solution.clients.config.validate_environment()"

clean: ## Clean up cache files and temporary data
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Workshop Exercises - MCP Fundamentals
workshop-fundamentals: ## Run MCP message structure exercises
	@echo "📋 Running MCP Fundamentals: Message Structure"
	@echo "Complete the TODOs in workshop/examples/01_message_structure.py first!"
	uv run python workshop/examples/01_message_structure.py

workshop-math-server: ## Run math server building exercise
	@echo "🧮 Running Math Server Workshop"
	@echo "Complete the TODOs in workshop/examples/02_math_server.py first!"
	uv run python workshop/examples/02_math_server.py

# Workshop Exercises - Server Development
workshop-wikipedia: ## Run Wikipedia server building exercise
	@echo "📚 Running Wikipedia Server Workshop"
	@echo "Complete the TODOs in workshop/servers/wikipedia_server.py first!"
	uv run python workshop/servers/wikipedia_server.py

solution-wikipedia: ## Run the complete Wikipedia MCP server
	@echo "📚 Starting Wikipedia MCP server"
	@echo "Press Ctrl+C to stop"
	uv run python solution/servers/wikipedia_server.py

# Workshop Exercises - Client Development
workshop-client-1: ## Run Client Exercise 1: MCP Agent Setup
	@echo "🔧 Running Client Exercise 1: MCP Agent Setup"
	uv run python workshop/clients/01_agent_setup.py

workshop-client-2: ## Run Client Exercise 2: Chat Interface Logic
	@echo "💬 Running Client Exercise 2: Chat Interface Logic"
	uv run python workshop/clients/02_chat_logic.py

workshop-client-3: ## Run Client Exercise 3: Polish
	@echo "✨ Running Client Exercise 3: Polish"
	@echo "Complete the TODOs in workshop/clients/03_polish.py first!"
	uv run python workshop/clients/03_polish.py

solution-cli: ## Run the complete CLI client solution
	@echo "🏆 Running complete CLI solution"
	uv run python solution/clients/cli_client.py chat

dev: ## Start development environment (Jupyter Lab)
	@echo "🔬 Starting Jupyter Lab for tutorials"
	@echo "Navigate to tutorials/ folder to start"
	uv run jupyter lab

test: ## Run all tests
	@echo "🧪 Running tests..."
	uv run python -m pytest -v

lint: ## Run linting (Ruff)
	@echo "🔍 Running linter..."
	uv run ruff check .

format: ## Format code (Ruff)
	@echo "✨ Formatting code..."
	uv run ruff format .
