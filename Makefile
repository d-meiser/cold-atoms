init:
	pip install -r requirements.txt

test:
	nosetests --with-coverage --cover-package=coldatoms --logging-level=INFO

run-notebooks:
	cd examples && python run_notebooks.py && cd .

develop:
	python setup.py develop

install:
	pip install .

.PHONY: init test

