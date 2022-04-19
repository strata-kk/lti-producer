.DEFAULT_GOAL := help

SRC_DIRS = ./ltiproducer/ ./standalone/

###### Development

compile-requirements: ## Compile requirements files
	pip-compile --output-file=requirements/base.txt setup.cfg
	pip-compile --output-file=requirements/dev.txt --extra=dev setup.cfg
	pip-compile --output-file=requirements/production.txt --extra=prod setup.cfg

upgrade-requirements: ## Upgrade requirements files
	pip-compile --output-file=requirements/base.txt --upgrade setup.cfg
	pip-compile --output-file=requirements/dev.txt --upgrade --extra=dev setup.cfg
	pip-compile --output-file=requirements/production.txt --upgrade --extra=prod setup.cfg

requirements: ## Install Python requirements
	pip install -r requirements/base.txt

dev-requirements: ## Install Python requirements for development
	pip install -r requirements/dev.txt

production-requirements: ## Install Python requirements for production
	pip install -r requirements/production.txt

migrate:
	./standalone/producer/manage.py migrate

static:
	./standalone/producer/manage.py collectstatic -v 0 --noinput

test: test-lint test-unit test-types test-format  ## Run all tests by decreasing order of priority
.PHONY: test

test-format: ## Run code formatting tests
	black --check --diff ${SRC_DIRS}

test-lint: ## Run code linting tests
	pylint --errors-only --enable=unused-import,unused-argument ${SRC_DIRS}

test-types: ## Check type definitions
	mypy --ignore-missing-imports ${SRC_DIRS}

test-unit: ## Run unit tests
	python -m unittest discover tests

format: ## Format code automatically
	black ${SRC_DIRS}

producer: ## Run a development producer server
	./standalone/producer/manage.py runserver 0.0.0.0:9630

consumer: ## Run a simple consumer for testing/development purposes
	./standalone/consumer/manage.py runserver localhost:9631

worker: ## Run an asynchronous task worker
	./standalone/producer/manage.py run_huey

###### Additional commands

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

