PYTHON = python3

.PHONY:	setup run clean test debug liny lint-strict

install:
		poetry install

run:
		poetry run $(PYTHON) a_maze_ing.py

debug:
		poetry run $(PYTHON) -m pdb a_maze_ing.py

clean:
		poetry env remove --all
		-rm poetry.lock
		find . -type d -name "__pycache__" -exec rm -rf {} +
		find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
		poetry run flake8 .
		poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
		poetry run flake8 .
		poetry run mypy . --strict