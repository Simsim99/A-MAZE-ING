PYTHON = python3

.PHONY:	run clean debug lint lint-strict build

install:
		pip install poetry
		poetry install

run:
		poetry run $(PYTHON) a_maze_ing.py

build:
		poetry build
		cp dist/mazegen-*.whl .

debug:
		poetry run $(PYTHON) -m pdb a_maze_ing.py

clean:
		poetry env remove --all
		rm -rf dist/
		-rm poetry.lock
		find . -type d -name "__pycache__" -exec rm -rf {} +
		find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
		poetry run flake8 mazegen/*.py a_maze_ing.py
		poetry run mypy mazegen/*.py a_maze_ing.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
		poetry run flake8 mazegen/*.py a_maze_ing.py
		poetry run mypy mazegen/*.py a_maze_ing.py --strict
