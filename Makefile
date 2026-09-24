.PHONY: install test lint dev docker-build build-index upload-index cloud-bootstrap cloud-pull cloud-evidence

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

build-index:
	PYTHONPATH=. python scripts/build_retrieval_index.py

upload-index:
	PYTHONPATH=. python scripts/upload_retrieval_artifacts.py

cloud-bootstrap:
	bash scripts/cloudshell/bootstrap.sh

cloud-pull:
	bash scripts/cloudshell/pull_latest.sh

cloud-evidence:
	PYTHONPATH=. python scripts/cloudshell/run_evidence.py
