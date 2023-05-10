.PHONY: clean quality style

check_dirs := cm computenode headnode

all: clean run

clean: 
	@echo "Cleaning up"
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

run:
	docker compose up --scale computenode=4 --build

stop:
	docker compose down

exec-head:
	docker compose exec headnode bash

exec-compute:
	docker compose exec computenode bash

quality:
	@echo "Quality check"
	black --check --preview $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

style:
	black --preview $(check_dirs)
	isort $(check_dirs)
