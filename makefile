SHELL := /bin/bash

install:
	pip install -r requirements.txt

test:
	python3 -m unittest src/test.py

run:
	python3 src/main.py
	mkdir -p data/transform
	mv weather* ./data/transform

clean:
	rm -rf __pycache__ *.pyc
	rm -rf data/raw
	rm -rf data/transform