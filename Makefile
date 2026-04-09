# Astro-Oracle 3.0: Automation Makefile

.PHONY: run shell build test clean seed

run:
	uvicorn app.main:app --reload --port 8000

docker-run:
	docker-compose up --build

test:
	pytest tests/

seed:
	python scripts/seed_data.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache

install:
	pip install -r requirements.txt

help:
	@echo "Astro-Oracle 3.0 Commands:"
	@echo "  make run        - Start FastAPI development server"
	@echo "  make docker-run - Start full stack with Docker"
	@echo "  make test       - Run pytest suite"
	@echo "  make seed       - Ingest demo celestial data"
	@echo "  make install    - Install python dependencies"
