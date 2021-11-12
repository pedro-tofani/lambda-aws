clean:
	rm -rf .venv data .pytest_cache .coverage

init: clean
	pip install poetry
	poetry install
	pre-commit install
