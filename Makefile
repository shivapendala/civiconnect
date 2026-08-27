.PHONY: all install build run test lint clean docker-up docker-down

all: install build

install:
	@echo "Installing root dependencies..."
	npm install
	pip install -r backend/requirements.txt
	pip install -r ai-service/requirements.txt

build:
	@echo "Building all components..."
	npm run build --prefix web
	python -m compileall backend ai-service

run:
	@echo "Starting CivicConnect Platform..."
	python main.py all

test:
	@echo "Running backend and integration test suites..."
	pytest backend/accounts/tests backend/complaints/tests

lint:
	@echo "Linting Python and TypeScript codebase..."
	flake8 backend ai-service --max-line-length=120 --exclude=venv,migrations || true
	npm run lint --prefix web || true

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down -v

clean:
	rm -rf dist build *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
