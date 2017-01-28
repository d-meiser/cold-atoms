init:
	pip install -r requirements.txt

test:
	nosetests

run-notebooks:
	cd examples && python run_notebooks.py && cd .

develop:
	python setup.py develop

install:
	pip install .

.PHONY: init test

