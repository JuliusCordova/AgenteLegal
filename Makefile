.PHONY: install test lint dev docker-build

install:
	python -m pip install -r requirements.txt

test:
	pytest -q

lint:
	python -m compileall app tests

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

docker-build:
	docker build -t agente-legal:local .
