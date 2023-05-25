.PHONY: clean quality style

check_dirs := cm computenode headnode

all: clean run

clean: 
	@echo "Cleaning up"
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf drive/db/*
	rm -rf drive/*/cmlogs
	rm -rf drive/*/**/cmlogs

run:
	docker compose up --scale computenode=4 --build

stop:
	docker compose down

exec-head:
	@mkdir -p drive/home/${USER}
	@docker compose exec -w /home/${USER} headnode bash

quality:
	@echo "Quality check"
	black --check --preview $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs)

style:
	black --preview $(check_dirs)
	isort $(check_dirs)
