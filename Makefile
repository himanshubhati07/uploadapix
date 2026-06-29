install:
	pip install -r requirements.txt

run:
	bash start.sh

test:
	pytest tests/ -v --tb=short

seed:
	python seed.py
