init:
	pip install -r requirements.txt

test:
	nosetests

develop:
	python setup.py develop

install:
	python setup.py install

.PHONY: init test

