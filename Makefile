.PHONY: help clean_pycache tests run

help:
	@echo "Available commands:"
	@echo "  make clean_pycache - Clean Python cache"
	@echo "  make tests - Run tests"
	@echo "  make run - Run the application"

clean_pycache:
	./scripts/clean_pycache.sh

tests:
	python -m pytest -v

run:
	cd src && uvicorn main:app --reload