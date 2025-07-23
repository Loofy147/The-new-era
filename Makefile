# AI Operating System Framework Makefile

.PHONY: help setup install run test clean build deploy docker-build docker-run

# Default target
help:
	@echo "AI Operating System Framework - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  setup     - Initial project setup"
	@echo "  install   - Install dependencies"
	@echo "  run       - Run the AI Operating System"
	@echo "  test      - Run test suite"
	@echo "  clean     - Clean temporary files"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-run    - Run with Docker Compose"
	@echo "  docker-stop   - Stop Docker containers"
	@echo ""
	@echo "Deployment:"
	@echo "  build     - Build for production"
	@echo "  deploy    - Deploy to production"
	@echo ""
	@echo "Utilities:"
	@echo "  lint      - Run code linting"
	@echo "  format    - Format code"
	@echo "  security  - Run security checks"

# Setup development environment
setup:
	@echo "🔧 Setting up AI Operating System Framework..."
	./scripts/setup.sh

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cd cli && npm install
	cd dashboard && npm install

# Run the system
run:
	@echo "🚀 Starting AI Operating System..."
	. venv/bin/activate && python main.py

# Run tests
test:
	@echo "🧪 Running test suite..."
	. venv/bin/activate && python tests/run_all_tests.py

# Run verification
verify:
	@echo "✅ Running system verification..."
	. venv/bin/activate && python verify_agents.py

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf node_modules
	rm -rf build
	rm -rf dist

# Build for production
build:
	@echo "🏗️ Building for production..."
	. venv/bin/activate && python -m compileall .
	cd dashboard && npm run build
	./scripts/deploy.sh production

# Docker commands
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-run:
	@echo "🐳 Running with Docker Compose..."
	docker-compose up -d

docker-stop:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "📜 Showing Docker logs..."
	docker-compose logs -f

# Development utilities
lint:
	@echo "🔍 Running code linting..."
	. venv/bin/activate && flake8 . --exclude=venv,node_modules
	cd cli && npm run lint
	cd dashboard && npm run lint

format:
	@echo "✨ Formatting code..."
	. venv/bin/activate && black . --exclude=venv
	cd cli && npm run format
	cd dashboard && npm run format

security:
	@echo "🔒 Running security checks..."
	. venv/bin/activate && python -c "from plugins.security_agent import SecurityHardeningAgent; agent = SecurityHardeningAgent(); agent.run()"

# CLI commands
cli:
	@echo "💻 Starting CLI..."
	cd cli && node src/index.js

dashboard:
	@echo "📊 Starting Dashboard..."
	cd dashboard && npm start

# Report generation
reports:
	@echo "📄 Generating reports..."
	. venv/bin/activate && python execute_all_agents.py

# System monitoring
status:
	@echo "📊 System Status:"
	. venv/bin/activate && python -c "from main import AIOperatingSystem; ai = AIOperatingSystem(); ai.initialize(); ai.show_system_status()"

# Quick development start
dev:
	@echo "🚀 Starting development environment..."
	make install
	make run

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	./scripts/deploy.sh production

# Environment setup
env:
	@echo "⚙️ Setting up environment file..."
	cp .env.example .env
	@echo "Please edit .env file with your configuration"

# Database setup (if using external database)
db-setup:
	@echo "🗄️ Setting up database..."
	. venv/bin/activate && python -c "from shared.utils import setup_database; setup_database()"

# Backup data
backup:
	@echo "💾 Creating backup..."
	tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz data/ reports/ config/

# Update dependencies
update:
	@echo "🔄 Updating dependencies..."
	. venv/bin/activate && pip install --upgrade -r requirements.txt
	cd cli && npm update
	cd dashboard && npm update

# Performance testing
perf:
	@echo "⚡ Running performance tests..."
	. venv/bin/activate && python -m pytest tests/performance/ -v

# Integration testing
integration:
	@echo "🔗 Running integration tests..."
	. venv/bin/activate && python -m pytest tests/integration/ -v
