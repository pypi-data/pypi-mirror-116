.PHONY: build

install:
	python3 -m pip install --user -q -r requirements.txt

build:
	docker build -q -t gm .

run: install build
	python3 main.py

test:
	pytest tests/

format:
	black --line-length 120 .