# Makefile for development workflow

# Default target
.DEFAULT_GOAL := help

# Virtualenv support (optional)
PYTHON := python3
PIP := pip3

help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PIP) install -r backend/requirements.txt

build: ## Build docker images
	docker-compose build

up: ## Start containers
	docker-compose up

down: ## Stop containers
	docker-compose down

restart: ## Restart containers
	docker-compose down && docker-compose up

test: ## Run tests with pytest
	PYTHONPATH=backend pytest backend/tests

lint: ## Run flake8 linter
	flake8 backend/

format: ## Format code using black
	black backend/

shell: ## Shell into backend container
	docker-compose exec backend sh

logs: ## Tail logs from all services
	docker-compose logs -f

migrate: ## Run db.create_all() manually
	docker-compose exec backend flask shell -c "from app import db, create_app; db.init_app(create_app()); db.create_all()"

health: ## Call backend health endpoint
	curl -s http://localhost:5000/health | jq

clean: ## Remove pycache and other junk
	find . -type d -name '__pycache__' -exec rm -r {} +; find . -name '*.pyc' -delete
